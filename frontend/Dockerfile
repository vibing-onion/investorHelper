# Use official Node.js image
FROM node:22

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy app code
COPY . .

# Expose port
EXPOSE 3000

# Start React app
# CMD ["npm", "run", "build"]
# CMD ["npm", "run", "preview"]
CMD ["npm", "run", "dev"]