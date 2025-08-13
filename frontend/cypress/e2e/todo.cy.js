describe('Logging into the system', () => {
  let uid // user id

  before(() => {
    cy.request({
      method: 'POST',
      url: 'http://localhost:5000/users/create',
      form: true,
      body: {
        firstName: 'wow12',
        lastName: 'wow12',
        email: 'wowsocool12@gmail.com'
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      uid = response.body._id.$oid
      console.log(response)
    });
  });

  beforeEach(() => {
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Login')
      .find('input[type=text]')
      .first()
      .type('wowsocool12@gmail.com');
    cy.get('form').submit();
  });

  describe('R8UC1 - User can create new task', () => {
    it('User can create new task', () => {
      cy.contains('div', 'Title')
        .find('input[type=text]')
        .type('Testing');

      cy.contains('div', 'YouTube URL')
        .find('input[type=text]')
        .type('dQw4w9WgXcQ&ab_channel=RickAstley');
      cy.get('form').submit();
    });
  });

  describe('R8UC1 - Create new task within the task', () => {
    it('User can add a new task with text', () => {
      cy.get('img').last().click();

      cy.get('ul.todo-list')
        .find('input[type=text]')
        .type('Get rickrolled');
      cy.get('form').last().submit();
    });
  });

  describe('R8UC1 Scenario 2 - Check if its possible to create a todo without a title', () => {
    it('Should handle empty task input gracefully', () => {
       cy.get('img').last().click();
       cy.get('form').last().within(() => {
        cy.get('input[type=submit]').should('disabled');
       });
    });
  });

  describe('R8UC2 Scenario: Todo item is unchecked — clicking marks it as checked', () => {
    it('User can click to check an unchecked todo item', () => {
      cy.get('img').last().click();
      cy.get('li.todo-item').last().within(() => {
        cy.get('span')
          .first()
          .should('exist')
          .and('have.class', 'checker unchecked')
          .then(($span) => {
            expect($span).not.to.have.class('checker checked');
            cy.wrap($span).click();
  
            cy.wrap($span).should('have.class', 'checker checked');
          });
      });
    });
  });

  describe('R8UC2 - Todo item is done - click on a already checked todo item', () => {
    it('User can click on item and it get unmarked', () => {
      cy.get('img').last().click();
      cy.get('li.todo-item').last().within(() => {
        cy.get('span')
          .first()
          .should('exist')
          .and('have.class', 'checker checked')
          .then(($span) => {
            expect($span).to.have.class('checker checked');
            cy.wrap($span).click();
  
            cy.wrap($span).should('have.class', 'checker unchecked');
          });
      })
    });
  });

  describe('R8UC3 - The user clicks the x-symbol to remove a todo item', () => {
    it('User can remove a todo item by clicking the remover span', () => {
      cy.get('img').last().click();
  
      cy.get('li.todo-item').then((itemsBefore) => {
        const countBefore = itemsBefore.length;
  
        cy.get('li.todo-item').last().within(() => {
          cy.get('span').should('exist').should('have.class', 'remover').last().click();
        });
  
        cy.get('li.todo-item').should('have.length', countBefore - 1);
      });
    });
  });

 after(() => {
  // First delete all tasks belonging to this user
  cy.request({
    method: 'GET',
    url: `http://localhost:5000/tasks/ofuser/${uid}`
  }).then((response) => {
    const tasks = response.body;
    
    // If tasks exist, delete them one by one
    tasks.forEach(task => {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/tasks/byid/${task._id.$oid}`
      });
    });
  }).then(() => {
    // Then delete the user
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    });
  });
});


});
