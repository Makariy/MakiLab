function RequestError(message) {                             
    this.message = message;
    this.name = "Server returned a response with status 'fail'";
    this.toString = () => {
        return this.args;
    }
} 
 
export default RequestError;