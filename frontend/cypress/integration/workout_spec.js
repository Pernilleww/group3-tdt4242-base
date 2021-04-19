
describe("Workout", () => {
    it('should create a planned workout', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();


        cy.get("#btn-plan-workout").click();


        cy.contains(" View/Edit Planned Workout");


        cy.get('input[name="name"]').type("Plan workout test").should("have.value", "Plan workout test");
        cy.get('textarea[name="notes"]').type("Plan workout test notes").should("have.value", "Plan workout test notes");


        //cy.get('#btn-add-exercise').click();
        cy.get('select[name="type"]').select("Plank", {force: true});
        cy.get('input[name="sets"]').type("3", {force: true}).should("have.value", "3");
        cy.get('input[name="number"]').type("3", {force: true}).should("have.value", "3");



        cy.get('input[name="date"]').type("2021-01-06T13:31");

        cy.get("#btn-ok-workout").click();


        cy.contains("Could not create new workout!");

        cy.contains("Date must be a future date");

        cy.get('input[name="date"]').type("2021-12-06T13:31");


        cy.get("#btn-ok-workout").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Owner: athlete");
        cy.contains("Plan workout test");
    });


    it('should create a logged workout', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();


        cy.get("#btn-create-workout").click();


        cy.contains(" View/Edit Logged Workout");


        cy.get('input[name="name"]').type("Log workout test").should("have.value", "Log workout test");
        cy.get('textarea[name="notes"]').type("Log workout test notes").should("have.value", "Log workout test notes");


        //cy.get('#btn-add-exercise').click();
        cy.get('select[name="type"]').select("Plank", {force: true});
        cy.get('input[name="sets"]').type("3", {force: true}).should("have.value", "3");
        cy.get('input[name="number"]').type("3", {force: true}).should("have.value", "3");



        cy.get('input[name="date"]').type("2021-06-06T13:31");

        cy.get("#btn-ok-workout").click();


        cy.contains("Could not create new workout!");

        cy.contains("Date must be an old date");

        cy.get('input[name="date"]').type("2021-01-06T13:31");


        cy.get("#btn-ok-workout").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Owner: athlete");
        cy.contains("Log workout test")
    });

    it('should edit a planned workout', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("My Planned Workouts").click();


        cy.contains("Plan workout test").click();


        cy.contains(" View/Edit Planned Workout");

        cy.get("#btn-edit-workout").click();


        cy.get('input[name="date"]').type("2021-01-06T13:31");

        cy.get("#btn-ok-workout").click();


        cy.contains("Could not update workout!");

        cy.contains("Date must be a future date");

        cy.get('input[name="date"]').type("2021-05-06T13:31");


        cy.get("#btn-ok-workout").click({force: true});


    });

    it('should edit a logged workout', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("My Logged Workouts").click();


        cy.contains("Log workout test").click({force: true});


        cy.contains(" View/Edit Logged Workout");

        cy.get("#btn-edit-workout").click();


        cy.get('input[name="date"]').type("2021-08-06T13:31");

        cy.get("#btn-ok-workout").click();


        cy.contains("Could not update workout!");

        cy.contains("Date must be an old date");

        cy.get('input[name="date"]').type("2021-01-06T13:31");


        cy.get("#btn-ok-workout").click({force: true});

    });

    it('should comment a logged workout', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("My Logged Workouts").click();


        cy.contains("Log workout test").click({force: true});


        cy.contains(" View/Edit Logged Workout");

        cy.get("#comment-area").type("This is a great workout", {force: true}).should("have.value", "This is a great workout");
        cy.get("#post-comment").click({force:true});

        cy.contains("Now");
        cy.contains("athlete");

        cy.get("#nav-workouts").should("be.visible").click({force: true});

        cy.contains("Log workout test").click({force: true});

        cy.contains("This is a great workout");



    });

    it('should delete a logged workout', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("My Logged Workouts").click();


        cy.contains("Log workout test").click({force: true});


        cy.contains(" View/Edit Logged Workout");

        cy.get("#btn-edit-workout").click();

        cy.get("#btn-delete-workout").click();

    });

    it('should delete a planned workout', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("My Logged Workouts").click();


        cy.contains("Plan workout test").click({force: true});


        cy.contains(" View/Edit Logged Workout");

        cy.get("#btn-edit-workout").click();

        cy.get("#btn-delete-workout").click();

    });

});