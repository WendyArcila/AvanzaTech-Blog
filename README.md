# AvanzaTechBlog: Blogging Platform with Django and REST API
AvanzaTechBlog is a powerful blogging platform built with Django,
designed to provide a comprehensive blogging and content management experience. 
With a focus on ease of use and versatility, 
AvanzaTechBlog offers the following key features:

  - Main Features
  Custom Blog Posts: Users can create, edit, and delete their 
  own blog posts intuitively and easily.
  
  - User Interaction: The platform allows users to 'like' and comment
  on other users' posts, encouraging interaction and engagement
  within the community.
  
  - Authentication and Permission Management: It offers a secure 
  and flexible authentication system, with defined user roles 
  (such as 'admin' and 'blogger') and granular access control 
  to posts
  
## Installation Instructions

## Project Structure

Project Structure
The AvanzaTechBlog project follows an organized structure based on the Model-View-Template (MVT) design pattern, which is the standard design pattern used by Django. This structure has been meticulously designed to facilitate understanding and development of the project. Below is a detailed description of the main directories and files:

- /avanzatech_blog: This main directory houses the main source code of the AvanzaTech Blog project. It is composed of the main application, which bears the same name, as well as 8 other applications that make up the project. This directory also contains a folder dedicated to tests for each application.

  * /avanzatech_blog: This folder contains the main application of the project. Here you will find global configuration files, such as settings.py, which defines the general configuration of the project, and the global project URLs.
  
  * /blog_post: This directory houses the application responsible for managing blog posts.
      - /api: Contains files that define pagination logic, serialization, and URLs related to posts.
      - views.py: File containing views related to posts.
      - models.py: File defining the model for posts.
      - j.json: File providing an example of the expected JSON format for this application.
  */category: Here is the application that manages post categories. These categories must be stored in the database.
      -/api: Contains files that define category serialization.
   	 	-models.py: File defining the model for categories.
  
  * /comment: Directory containing the application responsible for managing comments on posts.  
      - /api: Contains files that define pagination logic, serialization, and URLs related to comments.
      - views.py: File containing views related to comments.
      - models.py: File defining the model for comments.
  
  * /permission: Here is the application responsible for managing user permissions. These permissions must be recorded in the database before running the project.
     - /api: Contains files that define permission serialization.
     - models.py: File defining the model for permissions.

	*	/post_cat_permission: This directory contains the application that manages the relationship between posts, 
    categories, and permissions.
			 - /api: Contains files that define the relationship serialization.
			 - models.py: File defining the relationship model.
		
  * /post_like: Here is the application responsible for managing likes on posts.
			 - /api: Contains files that define pagination logic, serialization, and URLs related to likes.
			 - views.py: File containing views related to likes.
			 - models.py: File defining the model for likes.
 
	* /team: This directory houses the application responsible for managing teams.
		 - /api: Contains files that define team serialization.
		 - models.py: File defining the model for teams.
		 
	* /user: Here is the application responsible for managing users.
		 - /api: Contains files that define user serialization and related URLs.
		 - views.py: File containing views related to users.
		 - models.py: File defining the model for users.
			
	 * /tests: Directory containing tests for each application in the project.
			- /factories: Here are the factories segregated by applications for the tests.
			- /test_blogpost: Contains tests for the blog_post application.
			- /test_comment: Contains tests for the comment application.
			- /test_likes: Contains tests for the likes application.
			- /test_user: Contains tests for the user application.
			
	* /utilities: Directory containing utility files for different applications.
			- mixin.py: File containing the mixin for managing custom permissions for the application.
			- pagination.py: File with default project pagination configuration.

This organized structure ensures easy navigation and development of the project, facilitating efficient management of each component of the system.

## Project Usage

## API Documentation
