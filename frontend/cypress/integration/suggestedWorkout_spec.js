describe('The Home Page', () => {

    it('successfully login', () => {
        // this.currentUser will now point to the response
        // body of the cy.request() that we could use
        // to log in or work with in some way

        cy.visit("/login.html");

        cy.get('input[name="username"]').type("coach");
        cy.get('input[name="password"]').type("12345678")

        cy.get('#rememberMe').check();

        cy.get("#btn-login").click();

        cy.url().should('include', '/workouts.html');
    });

    it('should create a suggested workout', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("coach");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.url().should('include', '/workouts.html');

        cy.get("#btn-suggest-workout").click();

        cy.contains("Suggest Workout to Athlete")

        cy.get('input[name="name"]').type("Suggest workout test").should("have.value", "Suggest workout test");
        cy.get('textarea[name="notes"]').type("Suggest workout test notes").should("have.value", "Suggest workout test notes");
        cy.get('select[name="athlete"]').select("athlete");

        cy.get('select[name="type"]').select("Plank", {force: true});
        cy.get('input[name="sets"]').type("3", {force: true}).should("have.value", "3");
        cy.get('input[name="number"]').type("3", {force: true}).should("have.value", "3");

        cy.get("#btn-ok-workout").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Suggest workout test");

        cy.get("#btn-suggest-workout").click();

        cy.get('input[name="name"]').type("Suggest workout test - to decline").should("have.value", "Suggest workout test - to decline");
        cy.get('textarea[name="notes"]').type("Suggest workout test notes").should("have.value", "Suggest workout test notes");
        cy.get('select[name="athlete"]').select("athlete");


        cy.get("#btn-ok-workout").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Suggest workout test - to decline");

    });

    it('should cancel edit suggested workout', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("coach");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("Suggest workout test").click({force:true});

        cy.contains("Suggest Workout to Athlete")

        cy.get("#btn-edit-workout").click();

        cy.get('textarea[name="notes"]').clear().type("Suggest workout test notes edit").should("have.value", "Suggest workout test notes edit");

        cy.get("#btn-cancel-workout").click();

    });

    it('should edit suggested workout', function () {


        cy.visit("/login.html");

        cy.get('input[name="username"]').type("coach");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();


        cy.contains("Suggest workout test").click({force:true});



        cy.contains("Suggest Workout to Athlete")

        cy.get("#btn-edit-workout").click();
        cy.get('input[name="name"]').clear().type("Suggest workout test - edit").should("have.value", "Suggest workout test - edit");


        cy.get('textarea[name="notes"]').clear().type("Suggest workout test notes edit").should("have.value", "Suggest workout test notes edit");

        cy.get("#btn-ok-workout").click();

        cy.get('#nav-workouts').click({force: true});

        cy.contains("Suggest workout test - edit");
    });

    it('should be shown in "Suggested Workouts To Athletes"', function () {


        cy.visit("/login.html");

        cy.get('input[name="username"]').type("coach");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("Suggested Workouts To Athletes").click();

        cy.contains("Suggested Workout Seed");


    });

    it('should be shown in "Suggested Workouts From Coach"', function () {

        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("Suggested Workouts From Coach").click();

        cy.contains("Suggested Workout Seed");
    });

    it('should accept a suggested workout from coach', function () {


        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();


        cy.contains("Suggest workout test - edit").click({force:true});

        cy.contains("Suggest Workout to Athlete");

        cy.get('input[name="name"]').clear().type("Suggest workout test - accept").should("have.value", "Suggest workout test - accept");
        cy.get('textarea[name="notes"]').should("have.value", "Suggest workout test notes edit");

        cy.get('input[name="date"]').type("2021-01-06T13:31");

        cy.get("#btn-accept-workout").click();

        cy.contains("Could not create new workout!");

        cy.contains("Date must be a future date");


        cy.get('input[name="date"]').type("2021-11-06T13:31");


        cy.get("#btn-accept-workout").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Suggest workout test - accept")

        cy.contains("Owner: athlete");

        cy.contains("Suggest workout test - accept").click();

        cy.get("#btn-edit-workout").click();


        cy.get("#btn-delete-workout").click();


    });

    it('should decline a suggested workout from coach', function () {

        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();


        cy.contains("Suggest workout test - to decline").click({force:true});

        cy.contains("Suggested Workout from Coach");

        cy.get("#btn-decline-workout").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Suggest workout test - to decline").should('not.exist');
    });


})