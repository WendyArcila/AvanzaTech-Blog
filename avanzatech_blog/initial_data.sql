INSERT INTO team_team(name, description)
VALUES ('Default', 'This is the team by default');

INSERT INTO permission_permission(name, description)
VALUES ('ReadOnly', 'Can read but not edit');

INSERT INTO permission_permission(name, description)
VALUES ('Edit', 'Can read and edit');

INSERT INTO permission_permission(name, description)
VALUES ('None', 'Cannot read and edit');

INSERT INTO category_category(name, description)
VALUES ('Public', 'Unauthenticated user');

INSERT INTO category_category(name, description)
VALUES ('Authenticated', 'Authenticated user');

INSERT INTO category_category(name, description)
VALUES ('Team', 'User on the same team as the post author');

INSERT INTO category_category(name, description)
VALUES ('Author', 'Post author');

SELECT * from team_team; 