# Project-Medusa
## Instructions
Clone this repo 

Edit config.py with your DB connection URL (containing username/password) and encryption key
### build the 5 docker images located in the folders
 cd into each of the five folders and run the command "docker build -t name ." (replacing 'name' with the following names)   
    - medusa      
    - nginx      
    - ssh     
    - node_guacd    
    - frontend
  
 
 Open up the following ports on the security list, and firewall: 80, 3000
 Run "docker-compose up -d" from the Project-Medusa-r- directory 
    
