# build_files.sh
echo "Building Tailwind..."
npx @tailwindcss/cli -i ./static/input.css -o ./static/css/output.css --minify

echo "Collecting Static Files..."
python3.11 -m pip install -r requirements.txt
python3.11 manage.py collectstatic --noinput --clear