# Atlas Trafic API

Atlas Trafic API is a Django REST framework API that provides a set of endpoints for managing user data and performing traffic analysis.


## Installation and configuration

Make sure you have Python 3.10+ and pip installed. Then follow the steps below to set up your project.

1. Clone the repository:
```bash
git clone git@github.com:Igor-Pavlyshyn/Atlas_Trafic.git
cd Atlas_Trafic
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate (for linux and macOS)
venv/Scripts/activate (for windows)
```

3. Install the project dependencies:
```bash
pip install -r requirements.txt
```

4. Log in to ethereal.email:
- Go to [ethereal.email](https://ethereal.email/) and sign up for an account.
- Obtain the email and password credentials for the project.

5. Create the `.env` configuration file:
- Copy the contents of the `.env.sample` file and paste them into a new file named `.env`.
- Replace the placeholders with the actual values obtained from ethereal.email.

## Code Structure

The project is structured as follows:

- `Atlas_Trafic_API/`: This directory contains the main Django project.
- `user/`: This directory contains the code for the user app.
 - `models.py`: Defines the user model.
 - `views.py`: Defines the views for user-related endpoints.
 - `serializers.py`: Defines the serializers for user data.
- `atlas_trafic_app/`: This directory contains the code for the atlas_trafic_app app.
 - `models.py`: Defines the models for traffic analysis.
 - `views.py`: Defines the views for traffic analysis endpoints.
 - `serializers.py`: Defines the serializers for traffic analysis data.
 - `management/`: This directory contains management commands for the project.
   - `commands/`: This directory contains custom management commands.
     - `add_score_data.py`: A custom management command for adding score data.
     - `add_car_data.py`: A custom management command for adding car data.
     - `reset_score.py`: A custom management command for resetting score.
 - `urls.py`: Defines the URLs for the atlas_trafic_app app.
 - `apps.py`: Configures the atlas_trafic_app app.

## Features

- User Management:
- Sign up and login functionality.
- User profile management.

- Traffic Analysis:
- Real-time traffic data analysis.
- Traffic score calculation.
- Car detection and tracking.

## Running the Project

1. Make sure you have activated the virtual environment "(venv) should be displayed after your username in the terminal":
2. Run the development server:
```bash
python manage.py runserver
```
3. Access the API documentation at http://localhost:8000/api/schema/swagger/.
