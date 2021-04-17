let cancelWorkoutButton;
let okWorkoutButton;

function generateWorkoutForm() {
  var today = new Date().toISOString();

  document.querySelector("#inputDateTime").min = today;

  let form = document.querySelector("#form-workout");

  let formData = new FormData(form);
  let submitForm = new FormData();

  submitForm.append("name", formData.get("name"));
  let date = new Date(formData.get("date")).toISOString();
  submitForm.append("date", date);
  submitForm.append("notes", formData.get("notes"));
  submitForm.append("visibility", formData.get("visibility"));
  submitForm.append("planned", true);

  let exerciseInstances = [];
  let exerciseInstancesTypes = formData.getAll("type");
  let exerciseInstancesSets = formData.getAll("sets");
  let exerciseInstancesNumbers = formData.getAll("number");
  for (let i = 0; i < exerciseInstancesTypes.length; i++) {
    exerciseInstances.push({
      exercise: `${HOST}/api/exercises/${exerciseInstancesTypes[i]}/`,
      number: exerciseInstancesNumbers[i],
      sets: exerciseInstancesSets[i],
    });
  }

  submitForm.append("exercise_instances", JSON.stringify(exerciseInstances));
  for (let file of formData.getAll("files")) {
    submitForm.append("files", file);
  }
  return submitForm;
}

async function createWorkout() {
  let submitForm = generateWorkoutForm();

  let response = await sendRequest(
    "POST",
    `${HOST}/api/workouts/`,
    submitForm,
    ""
  );

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

async function createBlankExercise() {
  let exerciseTypeResponse = await sendRequest("GET", `${HOST}/api/exercises/`);
  let exerciseTypes = await exerciseTypeResponse.json();

  let exerciseTemplate = document.querySelector("#template-exercise");
  let divExerciseContainer = exerciseTemplate.content.firstElementChild.cloneNode(
    true
  );
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

function removeExercise() {
  let divExerciseContainers = document.querySelectorAll(
    ".div-exercise-container"
  );
  if (divExerciseContainers && divExerciseContainers.length > 0) {
    divExerciseContainers[divExerciseContainers.length - 1].remove();
  }
}


window.addEventListener("DOMContentLoaded", async () => {
  cancelWorkoutButton = document.querySelector("#btn-cancel-workout");
  okWorkoutButton = document.querySelector("#btn-ok-workout");
  let buttonAddExercise = document.querySelector("#btn-add-exercise");
  let buttonRemoveExercise = document.querySelector("#btn-remove-exercise");

  buttonAddExercise.addEventListener("click", createBlankExercise);
  buttonRemoveExercise.addEventListener("click", removeExercise);

  let currentUser = await getCurrentUser();

    await createBlankExercise();
    let ownerInput = document.querySelector("#inputOwner");
    ownerInput.value = currentUser.username;
    setReadOnly(false, "#form-workout");
    ownerInput.readOnly = !ownerInput.readOnly;

    okWorkoutButton.className = okWorkoutButton.className.replace(" hide", "");
    cancelWorkoutButton.className = cancelWorkoutButton.className.replace(
      " hide",
      ""
    );
    buttonAddExercise.className = buttonAddExercise.className.replace(
      " hide",
      ""
    );
    buttonRemoveExercise.className = buttonRemoveExercise.className.replace(
      " hide",
      ""
    );

    okWorkoutButton.addEventListener(
      "click",
      async () => createWorkout()
    );
    cancelWorkoutButton.addEventListener(
      "click",
      handleCancelDuringWorkoutCreate
    );
});
