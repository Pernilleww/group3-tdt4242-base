describe("Exercises", () => {
    it('should create an exercise', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678");

        cy.get('#rememberMe').check();

        cy.get("#btn-login").click();

        cy.get("#nav-exercises").should("be.visible").click();

        cy.get("#btn-create-exercise").click();

        cy.get("#inputName").type("Sit-up").should("have.value", "Sit-up");

        cy.get("#inputDescription").type("Lay on your back and lift your torso up. Should feel it in the stomach")
            .should("have.value", "Lay on your back and lift your torso up. Should feel it in the stomach");


        cy.get("#inputUnit").type("Sets").should("have.value", "Sets");

        cy.get("#btn-ok-exercise").click();
        cy.url().should('include', '/exercises.html');

        cy.contains("Sit-up");

    });


    it('should create a logged workout with an exercise', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();


        cy.get("#btn-create-workout").click();


        cy.contains(" View/Edit Logged Workout");


        cy.get('input[name="name"]').type("Log workout test").should("have.value", "Log workout test");
        cy.get('textarea[name="notes"]').type("Log workout test notes").should("have.value", "Log workout test notes");

        cy.get('select[name="type"]').select("Sit-up", {force: true});
        cy.get('input[name="sets"]').type("3", {force: true}).should("have.value", "3");
        cy.get('input[name="number"]').type("3", {force: true}).should("have.value", "3");

        cy.get('input[name="date"]').type("2021-01-06T13:31");


        cy.get("#btn-ok-workout").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Owner: athlete");
        cy.contains("Log workout test");
    });

    it('should edit an exercise', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678");

        cy.get('#rememberMe').check();

        cy.get("#btn-login").click();

        cy.get("#nav-exercises").should("be.visible").click();

        cy.contains("Sit-up").click();

        cy.get("#btn-edit-exercise").click();

        cy.get("#inputName").type(" Edit").should("have.value", "Sit-up Edit");

        cy.get("#btn-ok-exercise").click();

    });


    it('should delete an exercise', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678");

        cy.get('#rememberMe').check();

        cy.get("#btn-login").click();

        cy.get("#nav-exercises").should("be.visible").click();

        cy.contains("Sit-up Edit").click();

        cy.get("#btn-edit-exercise").click();
        cy.get("#btn-delete-exercise").should("be.visible").click();

        cy.contains("Sit-up").should("not.exist");

    });



});