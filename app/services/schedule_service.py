import datetime
import io
import asyncio
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from typing import Dict, List
from dateutil.relativedelta import relativedelta

from app.entities.schedule_vigil import ScheduleVigilEntity
from app.entities.user import UserEntity
from app.interfaces.interfaces import IScheduleRepository
from app.exceptions.exceptions import ExcelParsingError, VigilsTypeNotFound, NoVigilsDataFromExcel
from app.models import ScheduleVigil


def parse_excel_sheets(file_bytes: bytes) -> Dict[str, Dict[any, any]]:
    """Читаем Excel и возвращаем простые структуры."""

    def safe_iat(df: pd.DataFrame, r: int, c: int):
        """Безопасный доступ к df.iat — возвращает None если вне границ."""
        if r is None or c is None:
            return None
        n_rows, n_cols = df.shape
        if r < 0 or c < 0 or r >= n_rows or c >= n_cols:
            return None
        return df.iat[r, c]

    with pd.ExcelFile(io.BytesIO(file_bytes)) as xls:
        df_sheet_settings = pd.read_excel(xls, sheet_name="Настройка графика", header=None)
        df_sheet_vigils_summer = pd.read_excel(xls, sheet_name="Календарь нарядов (ЛЕТ)", header=None)
        df_sheet_vigils_winter = pd.read_excel(xls, sheet_name="Календарь нарядов (ЗИМ)", header=None)

    try:
        # ---- стартовая дата из листа Настроек----
        matches = df_sheet_settings[df_sheet_settings.eq("Начальная дата календаря нарядов")].stack().index
        if len(matches) == 0:
            raise ExcelParsingError("Не найдена ячейка 'Начальная дата календаря нарядов' на листе 'Настройка графика'")
        start_pos = matches[0]
        scheduler_start_at = safe_iat(df_sheet_settings, start_pos[0] + 1, start_pos[1])
        if scheduler_start_at is None or pd.isna(scheduler_start_at):
            raise ExcelParsingError("Начальная дата календаря нарядов не найдена или пуста (лист 'Настройка графика')")

        # ---- второе вхождение для "Расписание ГК", т.к. первое вхождение содержит строку со всеми датами (неудобно парсить)----
        matches_gk = df_sheet_settings[df_sheet_settings.eq("Расписание ГК")].stack().index
        if len(matches_gk) < 2:
            raise ExcelParsingError("Не найдено второе вхождение 'Расписание ГК' (лист 'Настройка графика')")
        gk_pos = matches_gk[1]

        # собираем даты ГК справа снизу от найденной ячейки
        g_c_dates = []
        for offset in range(0, 10):
            val = safe_iat(df_sheet_settings, gk_pos[0] + 1, gk_pos[1] + offset)
            if val is None or pd.isna(val):
                break
            if isinstance(val, (datetime.datetime, pd.Timestamp)):
                g_c_dates.append(pd.to_datetime(val).to_pydatetime())
            else:
                break

        del df_sheet_settings

        # ---- График ответственных ----
        matches_resp = df_sheet_vigils_summer[df_sheet_vigils_summer.eq("График ответственных")].stack().index
        if len(matches_resp) == 0:
            raise ExcelParsingError("Не найдена ячейка 'График ответственных' (лист 'Календарь нарядов (ЛЕТ)')")
        resp_pos = matches_resp[0]

        scheduler_responsible = {}
        scheduler_current_date = scheduler_start_at
        n_rows_s, n_cols_s = df_sheet_vigils_summer.shape
        for offset in range(1, n_cols_s - resp_pos[1]):
            c = resp_pos[1] + offset
            val = safe_iat(df_sheet_vigils_summer, resp_pos[0], c)
            if val is None or pd.isna(val):
                break
            scheduler_responsible[scheduler_current_date.strftime("%d-%m-%Y")] = val
            scheduler_current_date += datetime.timedelta(days=1)

        # ---- Сбор ФИО -> должность (fios_post) из summer и winter ----
        matches_fio = df_sheet_vigils_summer[df_sheet_vigils_summer.eq("ФИО")].stack().index
        if len(matches_fio) == 0:
            raise ExcelParsingError("Не найдена ячейка 'ФИО' (лист 'Календарь нарядов (ЛЕТ)')")
        fio_pos = matches_fio[0]

        fios_summer_post = {}
        # summer: вниз от fio_pos (начиная с +3)
        n_rows_s, n_cols_s = df_sheet_vigils_summer.shape
        for dr in range(3, n_rows_s - fio_pos[0]):
            r = fio_pos[0] + dr
            val_name = safe_iat(df_sheet_vigils_summer, r, fio_pos[1])
            if val_name is None or pd.isna(val_name):
                break
            val_post = safe_iat(df_sheet_vigils_summer, r, fio_pos[1] + 1)
            fios_summer_post[val_name] = val_post


        fios_winter_post = {}
        # winter: тоже вниз от той же колонки (если есть)
        n_rows_w, n_cols_w = df_sheet_vigils_winter.shape
        for dr in range(3, n_rows_w - fio_pos[0]):
            r = fio_pos[0] + dr
            val_name = safe_iat(df_sheet_vigils_winter, r, fio_pos[1])
            if val_name is None or pd.isna(val_name):
                break
            val_post = safe_iat(df_sheet_vigils_winter, r, fio_pos[1] + 1)
            fios_winter_post[val_name] = val_post

        # ---- Поиск стартовой колонки дат нарядов ----
        matches_start_col = df_sheet_vigils_summer[df_sheet_vigils_summer.eq(scheduler_start_at)].stack().index
        if len(matches_start_col) == 0:
            raise ExcelParsingError("Не найдена ячейка с датой старта в 'Календарь нарядов (ЛЕТ)'")
        start_col_pos = matches_start_col[0]

        # считаем кол-во дат вправо
        n_rows_s, n_cols_s = df_sheet_vigils_summer.shape
        date_count = 1
        for offset in range(1, n_cols_s - start_col_pos[1]):
            c = start_col_pos[1] + offset
            val = safe_iat(df_sheet_vigils_summer, start_col_pos[0], c)
            if val is None or pd.isna(val):
                break
            date_count += 1
            if date_count > 200:
                raise ExcelParsingError(
                    "Ошибка в чтении дат нарядов: найдено подозрительно много дат (>200)."
                )


        summer_row_start = 2
        summer_row_end = 2 + len(fios_summer_post) + 1
        summer_col_start = start_col_pos[1]
        summer_col_end = date_count + start_col_pos[1]

        winter_row_start = 2
        winter_row_end = 2 + len(fios_winter_post) + 1
        winter_col_start = start_col_pos[1]
        winter_col__end = date_count + start_col_pos[1]


        summer_df = df_sheet_vigils_summer.iloc[summer_row_start:summer_row_end, summer_col_start:summer_col_end]
        summer_df.columns = summer_df.iloc[0]
        summer_df.columns.name = None
        summer_df = summer_df.drop(summer_df.index[0])

        summer_index = [safe_iat(df_sheet_vigils_summer, r, fio_pos[1])
                        for r in range(summer_row_start + 1, summer_row_end)]
        summer_df.index = pd.Index(summer_index, name="ФИО")
        summer_df.insert(0, "Должность", summer_df.index.map(fios_summer_post))

        del df_sheet_vigils_summer


        winter_df = df_sheet_vigils_winter.iloc[winter_row_start:winter_row_end, winter_col_start:winter_col__end]
        winter_df.columns = winter_df.iloc[0]
        winter_df.columns.name = None
        winter_df = winter_df.drop(winter_df.index[0])

        winter_index = [safe_iat(df_sheet_vigils_winter, r, fio_pos[1])
                        for r in range(winter_row_start + 1, winter_row_end)]
        winter_df.index = pd.Index(winter_index, name="ФИО")
        winter_df.insert(0, "Должность", winter_df.index.map(fios_winter_post))

        del df_sheet_vigils_winter

        summer_dates = list(summer_df.columns[1:])
        winter_dates = list(winter_df.columns[1:])
        if summer_dates != winter_dates:
            raise ExcelParsingError("Наборы дат в летнем и зимнем расписаниях не совпадают!")

        merged_df = pd.concat([summer_df, winter_df]).fillna(value=pd.NA)


        schedule_dict = {}
        for fio, row in merged_df.iterrows():
            position = row.iloc[0]
            schedule = {
                str(date)[:10]: (None if pd.isna(val) else val)
                for date, val in row.iloc[1:].items()
            }
            schedule_dict[str(fio).strip()] = {
                "position": str(position) if not pd.isna(position) else None,
                "schedule": schedule
            }

        result_dict = {
            "schedule_vigils" : schedule_dict,
            "schedule_responsible" : scheduler_responsible,
            "gc_schedule": g_c_dates
        }

        return result_dict

    except Exception as e:
        raise ExcelParsingError(f"Таблица графиков была изменена, ошибка чтения данных: {e}")


class ScheduleService:
    def __init__(self, schedule_repo: IScheduleRepository):
        self.schedule_repo = schedule_repo

    async def get_vigils(self, **kwargs) -> List[ScheduleVigilEntity]:
        resp_vigil_id = await self.schedule_repo.get_vigils_type(name=["Ответственный"])
        if resp_vigil_id:
            kwargs["ignore_id"] = resp_vigil_id[0].id
        return await self.schedule_repo.get_vigils(**kwargs)


    async def create_vigils(self, info: Dict[str, Dict[str, str]], users: list[UserEntity]):
        """"Обработка данных из Excel и создание записей в таблицах График группы контроля, График нарядов"""
        try:
            vigils_type = await self.schedule_repo.get_vigils_type()
        except VigilsTypeNotFound:
            raise
        except Exception as e:
            raise e

        vigils = info.get("schedule_vigils")
        responsible = info.get("schedule_responsible")
        group_control = info.get("gc_schedule")
        if vigils:
            user_map = {u.short_name_2: u.id for u in users}

            vigils_by_id = {
                user_map[fio]: data
                for fio, data in vigils.items()
                if fio in user_map
            }

            if not vigils_by_id:
                raise NoVigilsDataFromExcel(
                    "В базе не нашлось ни одного пользователя с соответствующим именем из таблицы наряда"
                )

            all_vigils_dates = [
                datetime.datetime.strptime(date, "%Y-%m-%d")
                for v in vigils_by_id.values()
                for date in v["schedule"].keys()
            ]
            vigils_min_date = min(all_vigils_dates) if all_vigils_dates else None
            vigils_max_date = max(all_vigils_dates) if all_vigils_dates else None

        else:
            raise NoVigilsDataFromExcel("Нет данных об нарядах в таблице (либо данные ошибочные), проверьте, что всем именам соответствуют реальные пользователи в системе")


        if responsible:
            user_map = {u.surname: u.id for u in users}
            filtered_responsible = {
                date: user_map[fio]
                for date, fio in responsible.items()
                if fio in user_map
            }
            if not filtered_responsible:
                    raise NoVigilsDataFromExcel("Нет данных об ответственных в таблице (либо данные ошибочные), проверьте, что всем именам соответствуют реальные пользователи в системе")

            all_resp_dates = [
                datetime.datetime.strptime(date, "%d-%m-%Y")
                for date in filtered_responsible.keys()
            ]
            resp_min_date = min(all_resp_dates) if all_resp_dates else None
            resp_max_date = max(all_resp_dates) if all_resp_dates else None
        else:
            raise NoVigilsDataFromExcel("Нет данных об ответственных в таблице (либо данные ошибочные), проверьте, что всем именам соответствуют реальные пользователи в системе")

        group_control = [i for i in group_control]
        gc_min_date = group_control[0].replace(day=1)
        gc_max_date = gc_min_date + relativedelta(months=1)


        await self.schedule_repo.save_group_control_schedule(group_control_schedule=group_control, start_date=gc_min_date, end_date=gc_max_date)
        await self.schedule_repo.save_responsible_schedule(responsible=filtered_responsible, start_date=resp_min_date, end_date=resp_max_date)
        await self.schedule_repo.save_vigils_schedule(vigils_schedule=vigils_by_id, start_date=vigils_min_date, end_date=vigils_max_date)

    async def process_vigils_schedule(self, file_bytes: bytes) -> Dict[str, Dict[any, any]]:
        """
        Асинхронно обрабатываем Excel, возвращаем словарь с датафреймами.
        """
        loop = asyncio.get_event_loop()

        try:
            with ProcessPoolExecutor(max_workers=2) as executor:
                result = await asyncio.wait_for(
                    loop.run_in_executor(executor, parse_excel_sheets, file_bytes),
                    timeout=10
                )
                return result
        except asyncio.TimeoutError:
            raise ExcelParsingError("Парсинг Excel завис, возможно файл нестандартный, проверьте файл и попробуйте позже")
        except ExcelParsingError as e:
            raise e
        except Exception as e:
            raise e
