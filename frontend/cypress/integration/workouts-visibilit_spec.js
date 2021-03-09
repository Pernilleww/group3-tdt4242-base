describe("Visibilty workouts", () => {

    it('should test that public workout is visible for coach', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("coach");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("Public Workouts").click();


        cy.contains("Workout Public - Coach")
    });

    it('should test that public workout is visible for athlete', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("athlete");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("Public Workouts").click();

        cy.contains("Workout Public - Coach")
        cy.contains("Owner: coach")

    });

    it('should test that only my workouts shows up in "My logged Workouts"', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("coach");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("My Logged Workouts").click();

        cy.contains("My Planned Workouts").click();
        cy.contains("My Logged Workouts").click();


        cy.contains("Owner: athlete").should("not.be.visible");

    });

    it('should test that athlete workouts shows up in "Athlete Workouts"', function () {
        cy.visit("/login.html");

        cy.get('input[name="username"]').type("coach");
        cy.get('input[name="password"]').type("12345678")

        cy.get("#btn-login").click();

        cy.contains("Athlete Workouts").click();
        cy.contains("My Planned Workouts").click();
        cy.contains("Athlete Workouts").click();



        cy.contains("Owner: athlete").should("be.visible");

    });
})