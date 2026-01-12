echo "Installing Node dependencies..."
npm install @tailwindcss/cli

echo "Creating static directories..."
mkdir -p static/css

echo "Building Tailwind..."
npx @tailwindcss/cli -i ./theme/input.css -o ./static/css/output.css --minify

echo "Installing Python dependencies..."
python3.11 -m pip install -r requirements.txt

echo "Collecting Static Files..."
python3.11 manage.py collectstatic --noinput --clear