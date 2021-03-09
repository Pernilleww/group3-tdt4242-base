describe("Boundary test - Phone number ", function () {
    it("Finds register page", function () {
        cy.visit("/register.html");
        cy.contains("Create Account");
    });

    beforeEach(() => {

        cy.visit("register.html");
        cy.get('form');

        cy.get('input[name="email"]').type("test@test.no").should("have.value", "test@test.no");
        cy.get('input[name="password"]').type("hei");
        cy.get('input[name="password1"]').type("hei");
        cy.get('input[name="country"]').type("nombia").should("have.value", "nombia");
        cy.get('input[name="city"]').type("lol").should("have.value", "lol");
        cy.get('input[name="street_address"]').type("lol").should("have.value", "lol");
    });

    it("Checks boundary value for max+ phone number", function () {
        cy.get('input[name="username"]').type("Testmax+phone").should("have.value", "Testmax+phone");
        cy.get('input[name="phone_number"]').type("9".repeat(51));
        cy.get("#btn-create-account").click();
        cy.contains("Registration failed!");
        cy.contains("Ensure this field has no more than 50 characters");
    });

    it("Checks boundary value for min- phone number", function () {
        cy.get('input[name="username"]').type("Testmin-phone").should("have.value", "Testmin-phone");

        cy.get('input[name="phone_number"]');
        cy.get("#btn-create-account").click();

        cy.contains("Registration failed!");
    });

    it("Checks if a user can write letters in phone number", function () {
        cy.get('input[name="username"]').type("Testletterphone").should("have.value", "Testletterphone");


        cy.get('input[name="phone_number"]').type("h".repeat(50));
        cy.get("#btn-create-account").click();

        cy.contains("Registration failed!");
        cy.contains("Phone number can't contain letters");

    });

    it("Checks boundary value for max", function () {

        cy.get('input[name="username"]').type("Testmaxphone").should("have.value", "Testmaxphone");


        cy.get('input[name="phone_number"]').type("9".repeat(50));
        cy.get("#btn-create-account").click();


        cy.url().should('include', '/workouts.html');

        cy.contains("Log out");
        cy.contains("SecFit");
    });

    it("Checks boundary value for min", function () {

        cy.get('input[name="username"]').type("Testminphone").should("have.value", "Testminphone");


        cy.get('input[name="phone_number"]').type("9".repeat(1));
        cy.get("#btn-create-account").click();


        cy.url().should('include', '/workouts.html');

        cy.contains("Log out");
        cy.contains("SecFit");
    });

});


describe("Boundary test - user name ", function () {
    it("Finds register page", function () {
        cy.visit("/register.html");
        cy.contains("Create Account");
    });

    beforeEach(() => {

        cy.visit("register.html");
        cy.get('form');

        cy.get('input[name="email"]').type("test@test.no").should("have.value", "test@test.no");
        cy.get('input[name="password"]').type("hei");
        cy.get('input[name="password1"]').type("hei");
        cy.get('input[name="country"]').type("nombia").should("have.value", "nombia");
        cy.get('input[name="city"]').type("lol").should("have.value", "lol");
        cy.get('input[name="street_address"]').type("lol").should("have.value", "lol");
        ;
    });

    it("Checks boundary value for max+ username", function () {
        cy.get('input[name="username"]').type("u".repeat(151)).should("have.value", "u".repeat(151));
        cy.get("#btn-create-account").click();
        cy.contains("Registration failed!");
        cy.contains("Ensure this field has no more than 150 characters");

    });

    it("Checks boundary value for min- username", function () {
        cy.get("#btn-create-account").click();
        cy.contains("Registration failed!");
        cy.contains("This field may not be blank.");
    });


    it("Checks boundary value for max username", function () {

        cy.get('input[name="username"]').type("u".repeat(150)).should("have.value", "u".repeat(150));
        cy.get("#btn-create-account").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Log out");
        cy.contains("SecFit");
    });

    it("Checks boundary value for min username", function () {

        cy.get('input[name="username"]').type("u".repeat(1)).should("have.value", "u".repeat(1));
        cy.get("#btn-create-account").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Log out");
        cy.contains("SecFit");
    });

});


describe("Boundary test - email ", function () {
    it("Finds register page", function () {
        cy.visit("/register.html");
        cy.contains("Create Account");
    });

    beforeEach(() => {

        cy.visit("register.html");
        cy.get('form');

        cy.get('input[name="password"]').type("hei");
        cy.get('input[name="password1"]').type("hei");
        cy.get('input[name="country"]').type("nombia").should("have.value", "nombia");
        cy.get('input[name="city"]').type("lol").should("have.value", "lol");
        cy.get('input[name="street_address"]').type("lol").should("have.value", "lol");
        ;
    });

    it("Checks boundary value for max+ email", function () {
        cy.get('input[name="username"]').type("emailmax+").should("have.value", "emailmax+");
        cy.get('input[name="email"]').type("u".repeat(243) + "@test.no").should("have.value", "u".repeat(243)+ "@test.no");

        cy.get("#btn-create-account").click();
        cy.contains("Registration failed!");
        cy.contains("Ensure this field has no more than 50 characters");

    });

    it("Checks boundary value for min- email", function () {
        cy.get("#btn-create-account").click();
        cy.contains("Registration failed!");
        cy.contains("This field may not be blank.");
    });


    it("Checks boundary value for max", function () {

        cy.get('input[name="username"]').type("emailmax").should("have.value", "emailmax");
        cy.get('input[name="email"]').type("u".repeat(242) + "@test.no").should("have.value", "u".repeat(242)+ "@test.no");

        cy.get("#btn-create-account").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Log out");
        cy.contains("SecFit");
    });

    it("Checks boundary value for min", function () {

        cy.get('input[name="username"]').type("emailmin").should("have.value", "emailmin");
        cy.get('input[name="email"]').type("n@n.no").should("have.value", "n@n.no");

        cy.get("#btn-create-account").click();

        cy.url().should('include', '/workouts.html');

        cy.contains("Log out");
        cy.contains("SecFit");
    });

});