""" This module defines methods for translating data pipelines."""
import warnings
from typing import Optional
from wkmigrate.activity_translators.activity_translator import translate_activity
from wkmigrate.trigger_translators.schedule_trigger_translator import translate_schedule_trigger
from wkmigrate.utils import append_system_tags


def translate(pipeline: dict) -> dict:
    """ Translates a data pipeline to a common object model.
        :parameter pipeline: Dictionary definition of the source pipeline
        :return: Dictionary definition of the target workflows"""
    if 'name' not in pipeline:
        warnings.warn(f'No pipeline name in source definition, setting to UNNAMED_WORKFLOW')
    # Translate the pipeline:
    translated_pipeline = {
        'name': pipeline.get('name', 'UNNAMED_WORKFLOW'),
        'schedule': translate_schedule_trigger(pipeline.get('trigger')),
        'tasks': _translate_activities(pipeline.get('activities')),
        'tags': append_system_tags(pipeline.get('tags'))
    }
    return translated_pipeline


def _translate_activities(activities: Optional[list[dict]]) -> Optional[list[dict]]:
    """ Translates a set of data factory pipeline activities to a common object model.
        :parameter activities: Source pipeline activities
        :return: Target pipeline activities
    """
    translated_activities = []
    for activity in activities:
        translated_activity = translate_activity(activity)
        if isinstance(translated_activity, tuple):
            translated_activities.append(translated_activity[0])
            translated_activities.extend(_translate_activities(translated_activity[1]))
            continue
        translated_activities.append(translated_activity)
    return translated_activities
