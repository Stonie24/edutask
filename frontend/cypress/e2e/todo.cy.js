beforeEach(() => {
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Login').find('input[type=text]')
    .first()
    .type('mon.doe@gmail.com');

    cy.get('form').submit();
  })

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
describe('R8UC1 Scenario 2 - Create new task within the task with no text input', () => {
    it('User can add a new task with text', () => {
        cy.get('img').last().click();
        cy.get('form').last().submit();
    });
});

// describe('R8UC2 Scenario todo item is active - click on an active todo item', () => {
//   it('User can add a new task with text', () => {
//       cy.get('img').last().click();
      
       
      
//     cy.get('ul.todo-list').find("span").first().should('have.class', 'checker unchecked');
    
//     cy.get('ul.todo-list').find('span')
//          .first().click();
// });
// });


describe('R8UC2 Scenario todo item is checked - click on an checked todo item', () => {
    it('User can click and it should ', () => {
        cy.get('img').last().click();
        cy.get('li.todo-item').last().within(() => {
            cy.get('span').first().click();
            cy.get('span').first().should('have.class', 'checker checked');
        })
         
        
    //   cy.get('ul.todo-list').find("span").first().should('have.class', 'checker unchecked');
      
    //   cy.get('ul.todo-list').find('span')
    //        .first().click();
  });
  });
