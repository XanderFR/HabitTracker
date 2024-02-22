import datetime
import uuid
from flask import Blueprint, current_app, render_template, request, url_for, redirect

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")


@pages.context_processor
def addCalcDateRange():
    def dateRange(start: datetime.datetime):
        # Prepares a list with the current day, the past 3 days, and the next 3 days
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": dateRange}


def todayAtMidnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


@pages.route("/")
def index():
    dateStr = request.args.get("date")  # If url has date string parameter, send selected date to backend of app
    if dateStr:
        selectedDate = datetime.datetime.fromisoformat(dateStr)
    else:
        selectedDate = todayAtMidnight()

    habitsOnDate = current_app.db.habits.find({"added": {"$lte": selectedDate}})

    completions = [
        habit["habit"]
        for habit in current_app.db.completions.find({"date": selectedDate})
    ]
    return render_template(
        "index.html",
        habits=habitsOnDate,
        title="Habit Tracker - Home",
        selected_date=selectedDate,
        comlpletions=completions
    )


@pages.route("/add", methods=["GET", "POST"])
def addHabit():
    today = todayAtMidnight()
    if request.method == "POST":  # Habit form POST request
        current_app.db.habits.insert_one(
            {"_id": uuid.uuid4().hex, "added": today, "name": request.form.get("habit")}
        )

    return render_template("addHabit.html", title="Habit Tracker - Add Habit", selected_date=today)


@pages.route("/complete", methods=["POST"])
def complete():
    # Prepare a date + habit + completion status data group
    dateString = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(dateString)
    current_app.db.completions.insert_one({"date": date, "habit": habit})

    return redirect(url_for("habits.index", date=dateString))

