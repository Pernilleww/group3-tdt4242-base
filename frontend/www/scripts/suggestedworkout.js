let cancelWorkoutButton;
let okWorkoutButton;
let deleteWorkoutButton;
let editWorkoutButton;
let postCommentButton;
let acceptWorkoutButton;
let declineWorkoutButton;
let athleteTitle;
let coachTitle;

async function retrieveWorkout(id, currentUser) {
    let workoutData = null;
    let response = await sendRequest("GET", `${HOST}/api/suggested-workout/${id}/`);


    if (!response.ok) {
        let data = await response.json();
        let alert = createAlert("Could not retrieve workout data!", data);
        document.body.prepend(alert);
    } else {
        workoutData = await response.json();
        let form = document.querySelector("#form-workout");
        let formData = new FormData(form);

        if (currentUser.id == workoutData.coach) {
            let suggestTypeSelect = await selectAthletesForSuggest(currentUser);
            suggestTypeSelect.value = workoutData.athlete;

        }


        for (let key of formData.keys()) {
            let selector = `input[name="${key}"], textarea[name="${key}"]`;
            let input = form.querySelector(selector);
            let newVal = workoutData[key];

            if (key == "owner") {
                input.value = workoutData.coach;
            }

            /*if (key == "date") {
                // Creating a valid datetime-local string with the correct local time
                let date = new Date(newVal);
                date = new Date(date.getTime() - (date.getTimezoneOffset() * 60 * 1000)).toISOString(); // get ISO format for local time
                newVal = date.substring(0, newVal.length - 1);    // remove Z (since this is a local time, not UTC)
            }*/
            if (key != "suggested_workout_files") {
                input.value = newVal;
            }
        }

        let input = form.querySelector("select:disabled");
        // files
        let filesDiv = document.querySelector("#uploaded-files");
        for (let file of workoutData.suggested_workout_files) {
            let a = document.createElement("a");
            a.href = file.file;
            let pathArray = file.file.split("/");
            a.text = pathArray[pathArray.length - 1];
            a.className = "me-2";
            filesDiv.appendChild(a);
        }

        // create exercises

        // fetch exercise types
        let exerciseTypeResponse = await sendRequest("GET", `${HOST}/api/exercises/`);
        let exerciseTypes = await exerciseTypeResponse.json();

        //TODO: This should be in its own method.
        for (let i = 0; i < workoutData.suggested_exercise_instances.length; i++) {
            let templateExercise = document.querySelector("#template-exercise");
            let divExerciseContainer = templateExercise.content.firstElementChild.cloneNode(true);

            let exerciseTypeLabel = divExerciseContainer.querySelector('.exercise-type');
            exerciseTypeLabel.for = `inputExerciseType${i}`;

            let exerciseTypeSelect = divExerciseContainer.querySelector("select");
            exerciseTypeSelect.id = `inputExerciseType${i}`;
            exerciseTypeSelect.disabled = true;

            let splitUrl = workoutData.suggested_exercise_instances[i].exercise.split("/");
            let currentExerciseTypeId = splitUrl[splitUrl.length - 2];
            let currentExerciseType = "";

            for (let j = 0; j < exerciseTypes.count; j++) {
                let option = document.createElement("option");
                option.value = exerciseTypes.results[j].id;
                if (currentExerciseTypeId == exerciseTypes.results[j].id) {
                    currentExerciseType = exerciseTypes.results[j];
                }
                option.innerText = exerciseTypes.results[j].name;
                exerciseTypeSelect.append(option);
            }

            exerciseTypeSelect.value = currentExerciseType.id;

            let exerciseSetLabel = divExerciseContainer.querySelector('.exercise-sets');
            exerciseSetLabel.for = `inputSets${i}`;

            let exerciseSetInput = divExerciseContainer.querySelector("input[name='sets']");
            exerciseSetInput.id = `inputSets${i}`;
            exerciseSetInput.value = workoutData.suggested_exercise_instances[i].sets;
            exerciseSetInput.readOnly = true;

            let exerciseNumberLabel = divExerciseContainer.querySelector('.exercise-number');
            exerciseNumberLabel.for = "for", `inputNumber${i}`;
            exerciseNumberLabel.innerText = currentExerciseType.unit;

            let exerciseNumberInput = divExerciseContainer.querySelector("input[name='number']");
            exerciseNumberInput.id = `inputNumber${i}`;
            exerciseNumberInput.value = workoutData.suggested_exercise_instances[i].number;
            exerciseNumberInput.readOnly = true;

            let exercisesDiv = document.querySelector("#div-exercises");
            exercisesDiv.appendChild(divExerciseContainer);
        }
    }
    return workoutData;
}

function handleCancelDuringWorkoutEdit() {
    location.reload();
}

function handleEditWorkoutButtonClick() {
    let addExerciseButton = document.querySelector("#btn-add-exercise");
    let removeExerciseButton = document.querySelector("#btn-remove-exercise");

    setReadOnly(false, "#form-workout");

    let dateInput = document.querySelector("#inputDateTime");
    dateInput.readOnly = !dateInput.readOnly;

    document.querySelector("#inputOwner").readOnly = true;


    editWorkoutButton.className += " hide";
    okWorkoutButton.className = okWorkoutButton.className.replace(" hide", "");
    cancelWorkoutButton.className = cancelWorkoutButton.className.replace(" hide", "");
    deleteWorkoutButton.className = deleteWorkoutButton.className.replace(" hide", "");
    addExerciseButton.className = addExerciseButton.className.replace(" hide", "");
    removeExerciseButton.className = removeExerciseButton.className.replace(" hide", "");

    cancelWorkoutButton.addEventListener("click", handleCancelDuringWorkoutEdit);

}

async function deleteSuggestedWorkout(id) {
    let response = await sendRequest("DELETE", `${HOST}/api/suggested-workout/${id}/`);
    if (!response.ok) {
        let data = await response.json();
        let alert = createAlert(`Could not delete workout ${id}!`, data);
        document.body.prepend(alert);
    } else {
        window.location.replace("workouts.html");
    }
}

async function updateWorkout(id) {
    let submitForm = generateSuggestWorkoutForm();

    let response = await sendRequest("PUT", `${HOST}/api/suggested-workout/${id}/`, submitForm, "");
    if (response.ok) {
        location.reload();

    } else {
        let data = await response.json();
        let alert = createAlert("Could not update workout!", data);
        document.body.prepend(alert);
    }
}


async function acceptWorkout(id) {
    let submitForm = generateWorkoutForm();

    let response = await sendRequest("POST", `${HOST}/api/workouts/`, submitForm, "");

    if (response.ok) {
        await deleteSuggestedWorkout(id);
        window.location.replace("workouts.html");
    } else {
        let data = await response.json();
        let alert = createAlert("Could not create new workout!", data);
        document.body.prepend(alert);
    }
}

function generateWorkoutForm() {
    let form = document.querySelector("#form-workout");

    let formData = new FormData(form);
    let submitForm = new FormData();

    submitForm.append("name", formData.get('name'));
    let date = new Date(formData.get('date')).toISOString();
    submitForm.append("date", date);
    submitForm.append("notes", formData.get("notes"));
    //submitForm.append("owner", formData.get("coach_username"));
    submitForm.delete("athlete");
    submitForm.append("visibility", "CO");

    // adding exercise instances
    let exerciseInstances = [];
    let exerciseInstancesTypes = formData.getAll("type");
    let exerciseInstancesSets = formData.getAll("sets");
    let exerciseInstancesNumbers = formData.getAll("number");
    for (let i = 0; i < exerciseInstancesTypes.length; i++) {
        exerciseInstances.push({
            exercise: `${HOST}/api/exercises/${exerciseInstancesTypes[i]}/`,
            number: exerciseInstancesNumbers[i],
            sets: exerciseInstancesSets[i]
        });
    }

    submitForm.append("exercise_instances", JSON.stringify(exerciseInstances));
    // adding files
    for (let file of formData.getAll("files")) {
        submitForm.append("suggested_workout_files", file);
    }

    submitForm.append("planned", true);
    return submitForm;
}

function generateSuggestWorkoutForm() {
    let form = document.querySelector("#form-workout");

    let formData = new FormData(form);
    let submitForm = new FormData();

    submitForm.append("name", formData.get('name'));
    //let date = new Date(formData.get('date')).toISOString();
    //submitForm.append("date", date);
    submitForm.append("notes", formData.get("notes"));
    submitForm.append("athlete", formData.get("athlete"));
    submitForm.append("status", "p");



    // adding exercise instances
    let exerciseInstances = [];
    let exerciseInstancesTypes = formData.getAll("type");
    let exerciseInstancesSets = formData.getAll("sets");
    let exerciseInstancesNumbers = formData.getAll("number");

    for (let i = 0; i < exerciseInstancesTypes.length; i++) {
        exerciseInstances.push({
            exercise: `${HOST}/api/exercises/${exerciseInstancesTypes[i]}/`,
            number: exerciseInstancesNumbers[i],
            sets: exerciseInstancesSets[i]
        });
    }

    submitForm.append("suggested_exercise_instances", JSON.stringify(exerciseInstances));
    // adding files
    for (let file of formData.getAll("files")) {
        if (file.name != "") {
            submitForm.append("suggested_workout_files", file);
        }
    }


    return submitForm;
}

async function createSuggestWorkout() {
    let submitForm = generateSuggestWorkoutForm();


    let response = await sendRequest("POST", `${HOST}/api/suggested-workouts/create/ `, submitForm, "");

    if (response.ok) {
        window.location.replace("workouts.html");
    } else {
        let data = await response.json();
        let alert = createAlert("Could not create new workout!", data);
        document.body.prepend(alert);
    }
}

function handleCancelDuringWorkoutCreate() {
    window.location.replace("workouts.html");
}

async function selectAthletesForSuggest(currentUser) {

    let suggestTypes = [];
    let suggestTemplate = document.querySelector("#template-suggest");
    let divSuggestContainer = suggestTemplate.content.firstElementChild.cloneNode(true);
    let suggestTypeSelect = divSuggestContainer.querySelector("select");
    suggestTypeSelect.disabled = true;

    for (let athleteUrl of currentUser.athletes) {
        let response = await sendRequest("GET", athleteUrl);
        let athlete = await response.json();

        suggestTypes.push(athlete)
    }


    for (let i = 0; i < suggestTypes.length; i++) {
        let option = document.createElement("option");
        option.value = suggestTypes[i].id;
        option.innerText = suggestTypes[i].username;
        suggestTypeSelect.append(option);
    }

    let currentSuggestType = suggestTypes[0];
    suggestTypeSelect.value = currentSuggestType.id;

    let divSuggestWorkout = document.querySelector("#div-suggest-workout");
    divSuggestWorkout.appendChild(divSuggestContainer);
    return suggestTypeSelect;
}

async function createBlankExercise() {
    let form = document.querySelector("#form-workout");

    let exerciseTypeResponse = await sendRequest("GET", `${HOST}/api/exercises/`);
    let exerciseTypes = await exerciseTypeResponse.json();

    let exerciseTemplate = document.querySelector("#template-exercise");

    let divExerciseContainer = exerciseTemplate.content.firstElementChild.cloneNode(true);

    let exerciseTypeSelect = divExerciseContainer.querySelector("select");

    for (let i = 0; i < exerciseTypes.count; i++) {
        let option = document.createElement("option");
        option.value = exerciseTypes.results[i].id;
        option.innerText = exerciseTypes.results[i].name;
        exerciseTypeSelect.append(option);
    }

    let currentExerciseType = exerciseTypes.results[0];
    exerciseTypeSelect.value = currentExerciseType.name;

    let divExercises = document.querySelector("#div-exercises");
    divExercises.appendChild(divExerciseContainer);
}

function removeExercise(event) {
    let divExerciseContainers = document.querySelectorAll(".div-exercise-container");
    if (divExerciseContainers && divExerciseContainers.length > 0) {
        divExerciseContainers[divExerciseContainers.length - 1].remove();
    }
}


window.addEventListener("DOMContentLoaded", async () => {
    cancelWorkoutButton = document.querySelector("#btn-cancel-workout");
    okWorkoutButton = document.querySelector("#btn-ok-workout");
    deleteWorkoutButton = document.querySelector("#btn-delete-workout");
    editWorkoutButton = document.querySelector("#btn-edit-workout");
    acceptWorkoutButton = document.querySelector("#btn-accept-workout");
    declineWorkoutButton = document.querySelector("#btn-decline-workout");
    coachTitle = document.querySelector("#coach-title");
    athleteTitle = document.querySelector("#athlete-title");
    let postCommentButton = document.querySelector("#post-comment");
    let buttonAddExercise = document.querySelector("#btn-add-exercise");
    let buttonRemoveExercise = document.querySelector("#btn-remove-exercise");

    buttonAddExercise.addEventListener("click", createBlankExercise);
    buttonRemoveExercise.addEventListener("click", removeExercise);

    const urlParams = new URLSearchParams(window.location.search);
    let currentUser = await getCurrentUser();


    if (urlParams.has('id')) {
        const id = urlParams.get('id');
        let workoutData = await retrieveWorkout(id, currentUser);


        if (workoutData["coach"] == currentUser.id) {
            coachTitle.className = coachTitle.className.replace("hide", "");


            editWorkoutButton.classList.remove("hide");
            editWorkoutButton.addEventListener("click", handleEditWorkoutButtonClick);
            deleteWorkoutButton.addEventListener("click", (async (id) => await deleteSuggestedWorkout(id)).bind(undefined, id));
            okWorkoutButton.addEventListener("click", (async (id) => await updateWorkout(id)).bind(undefined, id));
            postCommentButton.addEventListener("click", (async (id) => await createComment(id)).bind(undefined, id));
        }


        if (workoutData["athlete"] == currentUser.id) {
            athleteTitle.className = athleteTitle.className.replace("hide", "");
            setReadOnly(false, "#form-workout");

            document.querySelector("#inputOwner").readOnly = true;


            declineWorkoutButton.classList.remove("hide");
            acceptWorkoutButton.classList.remove("hide");

            declineWorkoutButton.addEventListener("click", (async (id) => await deleteSuggestedWorkout(id)).bind(undefined, id));
            acceptWorkoutButton.addEventListener("click", (async (id) => await acceptWorkout(id)).bind(undefined, id));
            postCommentButton.addEventListener("click", (async (id) => await createComment(id)).bind(undefined, id));
        }
    } else {
        await createBlankExercise();


        if (currentUser.athletes.length > 0) {
            await selectAthletesForSuggest(currentUser);
        } else {
            let alert = createAlert("Will no be able to suggest workout due to not having any athltes", undefined);
            document.body.prepend(alert);
        }

        setReadOnly(false, "#form-workout");
        let ownerInput = document.querySelector("#inputOwner");
        ownerInput.value = currentUser.username;
        ownerInput.readOnly = !ownerInput.readOnly;

        let dateInput = document.querySelector("#inputDateTime");
        dateInput.readOnly = !dateInput.readOnly;


        coachTitle.className = coachTitle.className.replace("hide", "");

        okWorkoutButton.className = okWorkoutButton.className.replace(" hide", "");
        cancelWorkoutButton.className = cancelWorkoutButton.className.replace(" hide", "");
        buttonAddExercise.className = buttonAddExercise.className.replace(" hide", "");
        buttonRemoveExercise.className = buttonRemoveExercise.className.replace(" hide", "");

        okWorkoutButton.addEventListener("click", (async (currentUser) => await createSuggestWorkout(currentUser)).bind(undefined, currentUser));
        cancelWorkoutButton.addEventListener("click", handleCancelDuringWorkoutCreate);
    }

});