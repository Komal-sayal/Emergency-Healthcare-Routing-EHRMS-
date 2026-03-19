# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 5173

# Run Vite dev server accessible outside the container
CMD ["npx", "vite", "--host", "0.0.0.0"]
