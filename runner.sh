#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR"/venv/bin/activate"

echo "Start update"
python $DIR"/manage.py" runscript update_from_shell > $DIR"/runner_update.log" 2>&1 &&

#echo "Start runner all mps"
#python $DIR"/manage.py" runscript all_persons_runner > $DIR"/runner_all_m.log" 2>&1  &
#echo "Start runner pgs"
#python $DIR"/manage.py" runscript pgs_runner > $DIR"/runner_pgs.log" 2>&1  &
#echo "Start runner sessions"
#python $DIR"/manage.py" runscript sessions_runner > $DIR"/runner_sessions.log" 2>&1  &
#echo "Start runner signle persons"
#python $DIR"/manage.py" runscript single_person_runner > $DIR"/runner_single.log" 2>&1  &

wait
echo "End update"
deactivate
