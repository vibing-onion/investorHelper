### Investor Helper
InvestorHelper is a locally hosted app to help investors reading 10Q reports of US stocks. It is a flask application to demonstrate financial statement filings from SEC api.

### Development Prcoess
Under revamp. 

### Quick Start:
Change directory to backend
`cd backend`
Create docker image & container for backend & Run it
`docker build -t backend .`
`docker container run -dp 5000:5000 -t backend`

Change directory to backend
`cd frontend`
Create docker image & container for backend & Run it
`docker build -t frontend .`
`docker container run --rm -p 3000:3000 frontend`