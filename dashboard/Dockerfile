FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

# Using npm install instead of npm ci since lockfile might not exist yet for user
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
