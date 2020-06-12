#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
if [ -z "$1" ]
then
      echo "Please add the lambda function name as the first argument."
fi
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
LAMBDA_FUNCTION_NAME=$1

cd $DIR/
[ ! -e function.zip ] || rm function.zip
zip function.zip -q -r9 lambda_function.py gymbot.py
cd v-env/lib/python3.8/site-packages/
zip -q -r9 ${OLDPWD}/function.zip .
cd $DIR
exec aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} --zip-file fileb://function.zip
