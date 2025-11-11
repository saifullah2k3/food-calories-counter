# Food Calories Counter

A comprehensive web application for tracking food intake, calculating nutritional values, and providing personalized nutrition recommendations using machine learning.

## Features

- 🍎 **Food Logging**: Easily log your daily food intake with quantity and unit tracking
- 📊 **Nutrition Analysis**: Calculate daily intake of calories, proteins, fats, and carbohydrates
- 🎯 **Nutrition Assessment**: Get feedback on your nutrition based on Recommended Dietary Allowances (RDA)
- 🤖 **ML-Powered Recommendations**: Receive personalized nutrition recommendations using Linear Regression
- 📈 **Trend Visualization**: Plot nutritional trends over time (calories, proteins, etc.)
- 💾 **Database Integration**: SQLite database for persistent data storage

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite3
- **Machine Learning**: scikit-learn (Linear Regression)
- **Data Visualization**: matplotlib
- **Frontend**: HTML templates (Flask templating)

## Project Structure

```
food-calories-counter/
├── food caliries counterr.py  # Main application code (all modules combined)
├── database.py                # Database operations (users, food items, logs)
├── analysis.py                # Nutrition calculation and assessment
├── ml_module.py               # Machine learning recommendations
├── main.py                    # Flask application routes
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/food-calories-counter.git
   cd food-calories-counter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Dependencies

- Flask
- scikit-learn
- numpy
- matplotlib
- sqlite3 (built-in with Python)

## Usage

### Logging Food Items
1. Navigate to the `/log` endpoint
2. Enter your user ID, select a food item, specify quantity and unit
3. Submit to log your food intake

### Viewing Summary
1. Navigate to `/summary/<user_id>/<date>` to view your daily nutritional summary
2. Get feedback on your nutrition intake
3. Receive ML-powered recommendations

### Database Schema

- **users**: Stores user information and calorie goals
- **food_items**: Contains food items with nutritional information
- **user_logs**: Tracks user food intake with dates and quantities

## Features in Detail

### Nutrition Calculation
The application calculates your daily nutritional intake based on:
- Calories
- Proteins (grams)
- Fats (grams)
- Carbohydrates (grams)

### Machine Learning Recommendations
Using Linear Regression, the system:
- Analyzes your historical food intake
- Predicts future calorie needs
- Provides personalized recommendations based on RDA values

### Nutrition Assessment
The system compares your intake against RDA values and provides feedback:
- Low intake warnings
- High intake warnings
- Optimal intake confirmations

## Future Enhancements

- [ ] User authentication and session management
- [ ] Food database with extensive nutritional information
- [ ] Advanced ML models for better predictions
- [ ] Mobile app integration
- [ ] Export data to CSV/JSON
- [ ] Multi-user support with user profiles
- [ ] Recipe suggestions based on nutritional goals

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Created as a university project for food and nutrition tracking.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

