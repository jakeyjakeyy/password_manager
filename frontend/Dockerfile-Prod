# Build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:lts-alpine as production-stage
WORKDIR /app
COPY --from=build-stage /app/dist ./dist
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "tcp://0.0.0.0:5173"]