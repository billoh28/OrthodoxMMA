# Running the OrthodoxAPI locally

## AWS RDS instance must be running
Enter the following command at a command prompt:  
`mysql -h orthodoxcred.c9omrl6fspnx.eu-west-1.rds.amazonaws.com -P 3306 -u USERNAME -p`  
Replace the `USERNAME` and enter password

## Getting API running locally you must have Go installed on device
1. Locate this current directory
2. Run: `go run main.go`
3. Listening and serving HTTP on :8080

## Running API in the background of the EC2 instance:
`nohup go run main.go &`  
  
The logs of the API can be found in `nohup.out` file in OrthodoxAPI directory

## To stop the process of the API in the background of the EC2 instance:
1. `ps -ef` and find the go lang process running in OrthodoxAPI directory
2. Using the process ID, `kill -9 PID`
