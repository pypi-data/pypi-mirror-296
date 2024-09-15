from .if_condition_activity_translator import translate_if_condition_activity
from .notebook_activity_translator import translate_notebook_activity
from .spark_jar_activity_translator import translate_spark_jar_activity
from .spark_python_activity_translator import translate_spark_python_activity


type_mapping = {
    'DatabricksNotebook': 'notebook_task',
    'DatabricksSparkJar': 'spark_jar_task',
    'DatabricksSparkPython': 'spark_python_task',
    'IfCondition': 'condition_task'
}

type_translators = {
    'DatabricksNotebook': translate_notebook_activity,
    'DatabricksSparkJar': translate_spark_jar_activity,
    'DatabricksSparkPython': translate_spark_python_activity,
    'IfCondition': translate_if_condition_activity
}
