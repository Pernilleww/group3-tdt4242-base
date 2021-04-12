async function fetchWorkouts(ordering) {
    let response = await sendRequest(
        "GET",
        `${HOST}/api/workouts/?ordering=${ordering}`
    );

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    } else {
        let data = await response.json();

        let workouts = data.results;
        let container = document.getElementById("div-content");
        workouts.forEach((workout) => {
            let templateWorkout = document.querySelector("#template-workout");
            let cloneWorkout = templateWorkout.content.cloneNode(true);

            let aWorkout = cloneWorkout.querySelector("a");
            aWorkout.href = `workout.html?id=${workout.id}`;
            aWorkout.id = `workout-${workout.id}`

            let h5 = aWorkout.querySelector("h5");
            h5.textContent = workout.name;

            let localDate = new Date(workout.date);

            let table = aWorkout.querySelector("table");
            let rows = table.querySelectorAll("tr");
            rows[0].querySelectorAll(
                "td"
            )[1].textContent = localDate.toLocaleDateString(); // Date
            rows[1].querySelectorAll(
                "td"
            )[1].textContent = localDate.toLocaleTimeString(); // Time
            rows[2].querySelectorAll("td")[1].textContent = workout.owner_username; //Owner
            rows[3].querySelectorAll("td")[1].textContent =
                workout.exercise_instances.length; // Exercises

            container.appendChild(aWorkout);
        });
        return workouts;
    }
}

async function fetchSuggestedWorkouts() {
    let responseSuggestAthlete = await sendRequest("GET", `${HOST}/api/suggested-workouts/athlete-list/`);
    let responseSuggestCoach = await sendRequest("GET", `${HOST}/api/suggested-workouts/coach-list/`);

    if (!responseSuggestCoach || !responseSuggestAthlete) {
        throw new Error(`HTTP error! status: ${responseSuggestAthlete.status || responseSuggestCoach.status}`);
    } else {
        let suggestWorkoutAthlete = await responseSuggestAthlete.json();
        let suggestWorkoutCoach = await responseSuggestCoach.json();

        let suggestedWorkouts = suggestWorkoutAthlete.concat(suggestWorkoutCoach);
        let container = document.getElementById('div-content');

        suggestedWorkouts.forEach(workout => {
            let templateWorkout = document.querySelector("#template-suggested-workout");
            let cloneWorkout = templateWorkout.content.cloneNode(true);

            let aWorkout = cloneWorkout.querySelector("a");
            aWorkout.href = `suggestworkout.html?id=${workout.id}`;
            aWorkout.id = `suggested-workout-${workout.id}`;

            let h5 = aWorkout.querySelector("h5");
            h5.textContent = workout.name;


            let table = aWorkout.querySelector("table");
            let rows = table.querySelectorAll("tr");
            rows[0].querySelectorAll("td")[1].textContent = workout.coach_username; //Owner
            rows[1].querySelectorAll("td")[1].textContent = workout.suggested_exercise_instances.length; // Exercises
            rows[2].querySelectorAll("td")[1].textContent = workout.status === "p" ? "Pending" : "Accept"; // Exercises


            container.appendChild(aWorkout);
        });

        return [suggestWorkoutAthlete, suggestWorkoutCoach];
    }

}


function createWorkout() {
    window.location.replace("workout.html");
}

function suggestWorkout() {
    window.location.replace("suggestworkout.html");
}

function planWorkout() {
    window.location.replace("plannedWorkout.html");
}

window.addEventListener("DOMContentLoaded", async () => {
    let createButton = document.querySelector("#btn-create-workout");
    let suggestButton = document.querySelector("#btn-suggest-workout");
    suggestButton.addEventListener("click", suggestWorkout);
    createButton.addEventListener("click", createWorkout);
    let planButton = document.querySelector("#btn-plan-workout");
    planButton.addEventListener("click", planWorkout);
    let ordering = "-date";

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("ordering")) {
        let aSort = null;
        ordering = urlParams.get("ordering");
        if (ordering == "name" || ordering == "owner" || ordering == "date") {
            let aSort = document.querySelector(`a[href="?ordering=${ordering}"`);
            aSort.href = `?ordering=-${ordering}`;
        }
    }

    let currentSort = document.querySelector("#current-sort");
    currentSort.innerHTML =
        (ordering.startsWith("-") ? "Descending" : "Ascending") +
        " " +
        ordering.replace("-", "");

    let currentUser = await getCurrentUser();
    // grab username
    if (ordering.includes("owner")) {
        ordering += "__username";
    }
    let workouts = await fetchWorkouts(ordering);
    let [athleteWorkout, coachWorkout] = await fetchSuggestedWorkouts();

    let allWorkouts = workouts.concat(athleteWorkout, coachWorkout);

    let tabEls = document.querySelectorAll('a[data-bs-toggle="list"]');
    for (let i = 0; i < tabEls.length; i++) {
        let tabEl = tabEls[i];
        tabEl.addEventListener("show.bs.tab", function (event) {
            let workoutAnchors = document.querySelectorAll(".workout");
            for (let j = 0; j < allWorkouts.length; j++) {
                // I'm assuming that the order of workout objects matches
                // the other of the workout anchor elements. They should, given
                // that I just created them.
                let workout = allWorkouts[j];
                let workoutAnchor = workoutAnchors[j];

                switch (event.currentTarget.id) {
                    case "list-my-logged-workouts-list":
                        if (workout.owner == currentUser.url && !workout.planned) {
                            workoutAnchor.classList.remove("hide");
                        } else {
                            workoutAnchor.classList.add("hide");
                        }

                        break;
                    case "list-my-planned-workouts-list":
                        if (workout.owner == currentUser.url && workout.planned) {
                            workoutAnchor.classList.remove("hide");
                        } else {
                            workoutAnchor.classList.add("hide");
                        }

                        break;
                    case "list-athlete-workouts-list":
                        if (
                            currentUser.athletes &&
                            currentUser.athletes.includes(workout.owner)
                        ) {
                            workoutAnchor.classList.remove("hide");
                        } else {
                            workoutAnchor.classList.add("hide");
                        }
                        break;
                    case "list-public-workouts-list":
                        if (workout.visibility == "PU") {
                            workoutAnchor.classList.remove("hide");
                        } else {
                            workoutAnchor.classList.add("hide");
                        }
                        break;
                    case "list-suggested-coach-workouts-list":
                        if (currentUser.coach) {
                            let coachID = currentUser?.coach?.split('/');
                            if (coachID[coachID.length - 2] == workout.coach) {
                                workoutAnchor.classList.remove('hide');

                            }
                        } else {
                            workoutAnchor.classList.add('hide');
                        }
                        break;
                    case "list-suggested-athlete-workouts-list":
                        let athletes = currentUser?.athletes?.map((athlete) => {
                            let athleteIdSplit = athlete.split('/');
                            return Number(athleteIdSplit[athleteIdSplit.length - 2]);

                        })
                        if (athletes.includes(workout.athlete)) {
                            workoutAnchor.classList.remove('hide');
                        } else {
                            workoutAnchor.classList.add('hide');
                        }
                        break;

                    default :
                        workoutAnchor.classList.remove("hide");
                        break;
                }
            }
        });
    }
});
