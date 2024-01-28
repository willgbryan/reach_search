FROM node:14

WORKDIR /usr/src/app

COPY reach-search-app/package*.json ./

RUN npm install

COPY reach-search-app .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]