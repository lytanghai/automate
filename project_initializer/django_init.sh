#!/usr/bin/bash

# Exit on any error
set -e

# --- Configuration ---

DJANGO_VERSION=5.2

# --- Input Args ---
DIR=$1
MODE=$2            # pipenv or pip
PROJECT_NAME=$3    # Django project name
APP_NAME=$4        # Django app name

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 'directory path' [pip|pipenv] 'project_name' 'app_name'"
  exit 1
fi

# --- Check Directory ---
if [ -e "$DIR" ]; then
    echo "✅ Path exists: $DIR"
    cd "$DIR"

    if [ -e "$PROJECT_NAME" ]; then
        echo "⚠️  Removing existing project directory: $PROJECT_NAME"
        rm -rf "$PROJECT_NAME"
    fi
else
    echo "❌ Path does not exist: $DIR"
    exit 1
fi

# --- Create Project Directory ---
mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"

# --- Environment Setup ---
if [ "$MODE" == "pipenv" ]; then
  echo "📦 Initializing pipenv environment..."
  version=$(python --version 2>&1 | cut -d ' ' -f2)
  pipenv --python "$version"
  pipenv install django==$DJANGO_VERSION
  RUN_CMD="pipenv run"
elif [ "$MODE" == "pip" ]; then
  echo "📦 Using system environment with venv..."
  python3 -m venv venv
  source venv/bin/activate
  pip install django==$DJANGO_VERSION
  RUN_CMD=""
else
  echo "❌ Invalid mode: must be 'pip' or 'pipenv'"
  exit 1
fi

# --- Create Django Project & App ---
$RUN_CMD django-admin startproject "$PROJECT_NAME" .
$RUN_CMD python manage.py startapp "$APP_NAME"

# --- Create Views Directory ---
mkdir -p "$APP_NAME/views"
touch "$APP_NAME/views/__init__.py"

# --- Create Template & Static Folders ---
mkdir -p "$APP_NAME/templates/$APP_NAME"
mkdir -p "$APP_NAME/static/css" "$APP_NAME/static/js" "$APP_NAME/static/img"
touch "$APP_NAME/templates/$APP_NAME/index.html"
touch "$APP_NAME/static/css/style.css"
touch "$APP_NAME/static/js/main.js"
touch "$APP_NAME/static/img/.gitkeep"

# --- Create sample view ---
cat <<EOF > "$APP_NAME/views/home.py"
from django.shortcuts import render

def index(request):
    return render(request, '$APP_NAME/index.html')
EOF

# --- Create urls.py for app ---
cat <<EOF > "$APP_NAME/urls.py"
from django.urls import path
from .views import home

urlpatterns = [
    path('', home.index, name='home'),
]
EOF

# --- Add app to INSTALLED_APPS ---
SETTINGS_FILE="$PROJECT_NAME/settings.py"
if ! grep -q "'$APP_NAME'" "$SETTINGS_FILE"; then
  sed -i "/INSTALLED_APPS = \[/ a\    '$APP_NAME'," "$SETTINGS_FILE"
  echo "✅ Added '$APP_NAME' to INSTALLED_APPS"
fi

# --- Include app URLs in project urls.py ---
PROJECT_URLS="$PROJECT_NAME/urls.py"
if ! grep -q "include" "$PROJECT_URLS"; then
  sed -i "1 afrom django.urls import include, path" "$PROJECT_URLS"
fi

if ! grep -q "$APP_NAME.urls" "$PROJECT_URLS"; then
  sed -i "/urlpatterns = \[/ a\    path('', include('$APP_NAME.urls'))," "$PROJECT_URLS"
  echo "✅ Routed '$APP_NAME/urls.py' in $PROJECT_URLS"
fi

# --- Done ---
echo "🎉 Django project '$PROJECT_NAME' with app '$APP_NAME' initialized."

if [ "$MODE" == "pipenv" ]; then
  echo "👉 To activate your environment again: pipenv shell"
else
  echo "👉 To activate your environment again: source venv/bin/activate"
fi
