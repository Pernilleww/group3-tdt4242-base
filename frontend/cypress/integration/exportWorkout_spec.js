it('should export a planned workout', function () {
    cy.visit("/login.html");

    cy.get('input[name="username"]').type("coach");
    cy.get('input[name="password"]').type("hei")

    cy.get("#btn-login").click();


    cy.get("#workout-1").click({force: true});


    cy.contains(" View/Edit Planned Workout");

    const expectedHeaders = ["Subject", "Start date", "Start time", "Description"];

    cy.get("#btn-export-workout").should("be.visible").click();

    cy.readFile("cypress/downloads/event.csv").then(text => {
        const content = text.split(",")
        const headers = content.splice(0, 4);
        let descriptionAndSubjectNameInOne = headers.pop();
        let descriptionAndSubjectArray = descriptionAndSubjectNameInOne.split("\n");
        let description = descriptionAndSubjectArray[0];
        description = description.substring(0, description.length - 1);
        let subjectName = descriptionAndSubjectArray[1];
        headers.push(description);
        content.unshift(subjectName);

        let descriptionContent = content.pop();
        descriptionContent = descriptionContent.substring(0, descriptionContent.length - 2);
        content.push(descriptionContent);

        expect(headers).deep.to.equal(expectedHeaders);

        const csvDate = `${content[1]} ${content[2]}`
        let date = new Date(csvDate);



        date = new Date(date.getTime() - date.getTimezoneOffset() * 60 * 1000).toISOString(); // get ISO format for local time
        date = date.substring(0, date.length - 5); // remove Z (since this is a local time, not UTC)


        cy.get('input[name="name"]').should("have.value", content[0]);
        cy.get('input[name="date"]').should("have.value", date);
        cy.get('textarea[name="notes"]').should("have.value", content[3]);


    })


});
