# To start docker swam:

## 1. Push images to the image repository if they're not there yet:

## 2. Initialize a Swarm

`docker swarm init`

###### Machine running this command will act as the manager node.

## 3. Create an Overlay Network:

Open your terminal and run the following command to create a swarm-scoped overlay network:
`docker network create --driver overlay my-overlay-network`

###### This is essential in Docker Swarm mode as it allows containers across different Docker hosts to communicate with each other.

## 4. Verify the Network:

You can check if the network has been created successfully by listing all networks:

`docker network ls`

###### Look for my-overlay-network in the list with the driver set to overlay.

## 5. Deploy the Stack:

Once the network is set up, you can go ahead and deploy your stack:

`docker stack deploy -c docker-swarm.yaml myapp`