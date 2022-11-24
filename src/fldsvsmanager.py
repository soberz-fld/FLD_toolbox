import schedule
import threading
import types

from fldlogging import log


def _run_in_new_thread(job_function) -> None:
    job_thread = threading.Thread(target=job_function)
    job_thread.start()


def module_initializer(list_of_instances: list) -> None:
    """
    Initializes moduls to run scheduled.
    :param list_of_instances: Three kinds of tuple:
        - (instance, every_x_seconds)
        - (instance, time_value, time_unit)
        - (instance, day_kind, at_hour, at_minute, at_second)
    :return: None
    """
    for instance_tuple in list_of_instances:
        try:
            job = None
            if len(instance_tuple) == 2:  # Job every x seconds
                job = schedule.every(instance_tuple[1]).seconds.do(_run_in_new_thread, instance_tuple[0].run)
            elif len(instance_tuple) == 3:  # Job every x time units
                if isinstance(instance_tuple[0], types.ModuleType) and instance_tuple[1] > 0 and type(instance_tuple[2]) == str:
                    if instance_tuple[2] == 'seconds' and type(instance_tuple[1]) == int:
                        job = schedule.every(instance_tuple[1]).seconds.do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[2] == 'minutes' and type(instance_tuple[1]) == int:
                        job = schedule.every(instance_tuple[1]).minutes.do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[2] == 'hours' and type(instance_tuple[1]) == int:
                        job = schedule.every(instance_tuple[1]).hours.do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[2] == 'days' and type(instance_tuple[1]) == int:
                        job = schedule.every(instance_tuple[1]).days.do(_run_in_new_thread, instance_tuple[0].run)
                    else:
                        log(error='Did not schedule' + str(instance_tuple) + ' - time unit unknown')
                else:
                    log(error='Did not schedule' + str(instance_tuple) + ' - unknown tuple configuration')
            elif len(instance_tuple) == 5:  # Job at specific time
                if isinstance(instance_tuple[0], types.ModuleType) and type(instance_tuple[1]) == str and type(instance_tuple[2]) == int and type(instance_tuple[3]) == int and type(instance_tuple[4]) == int:
                    exec_time = str(instance_tuple[2]).zfill(2) + ':' + str(instance_tuple[3]).zfill(2) + ':' + str(instance_tuple[4]).zfill(2)
                    if instance_tuple[1] == 'day':
                        job = schedule.every().day.at(exec_time).do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[1] == 'monday':
                        job = schedule.every().monday.at(exec_time).do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[1] == 'tuesday':
                        job = schedule.every().tuesday.at(exec_time).do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[1] == 'wednesday':
                        job = schedule.every().wednesday.at(exec_time).do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[1] == 'thursday':
                        job = schedule.every().thursday.at(exec_time).do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[1] == 'friday':
                        job = schedule.every().friday.at(exec_time).do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[1] == 'saturday':
                        job = schedule.every().saturday.at(exec_time).do(_run_in_new_thread, instance_tuple[0].run)
                    elif instance_tuple[1] == 'sunday':
                        job = schedule.every().sunday.at(exec_time).do(_run_in_new_thread, instance_tuple[0].run)
                    else:
                        log(error='Did not schedule' + str(instance_tuple) + ' - day_kind unknown')
                else:
                    log(error='Did not schedule' + str(instance_tuple) + ' - unknown tuple configuration')
            else:
                log(error='Did not schedule' + str(instance_tuple) + ' - unknown tuple configuration, number of elements does not fit')
            if job:
                log(action='Scheduled ' + str(instance_tuple[0].__name__) + ': ' + str(job))
        except schedule.ScheduleValueError as e:
            log(error='Did not schedule' + str(instance_tuple) + ' - Error: ' + str(e))


def main_loop():
    while True:
        schedule.run_pending()
