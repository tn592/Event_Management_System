# build_files.sh

npm install @tailwindcss/cli


echo "Building Tailwind..."
npx @tailwindcss/cli -i ./theme/input.css -o ./static/css/output.css --minify

echo "Collecting Static Files..."
python3.11 -m pip install -r requirements.txt
python3.11 manage.py collectstatic --noinput --clear