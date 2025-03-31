//User friendly web server written in C
#include "thlib.c"
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <time.h>

#define PORT 6065
#define BUFFER_SIZE 1024

void serve_image(int client_socket, const char *image_path) {
    FILE *image = fopen(image_path, "rb");
    if (!image) {
        printf("Error opening image file: %s\n", image_path);
        return;
    }

    // Get the image file size
    fseek(image, 0, SEEK_END);
    long image_size = ftell(image);
    fseek(image, 0, SEEK_SET);

    // Read the image data into a buffer
    char *image_buffer = (char *)malloc(image_size);
    fread(image_buffer, 1, image_size, image);

    // Send HTTP response headers
    const char *http_header = "HTTP/1.1 200 OK\r\n";
    const char *content_type_header = "Content-Type: image/jpeg\r\n"; // Change this based on image type
    const char *connection_header = "Connection: close\r\n";
    
    write(client_socket, http_header, strlen(http_header));
    write(client_socket, content_type_header, strlen(content_type_header));
    write(client_socket, connection_header, strlen(connection_header));
    write(client_socket, "\r\n", 2); // End of headers

    // Send the image content (binary data)
    write(client_socket, image_buffer, image_size);

    // Clean up
    free(image_buffer);
    fclose(image);
}



int main()
{
	char buffer[BUFFER_SIZE];

	// Create a socket
	int sockfd = socket(AF_INET,SOCK_STREAM,0);
	if(sockfd == -1)
	{
		perror("webserver (socket)");
		return 1;
	}
	printf("socket created successfully\n");
	
	// Create address to bind the socket to
	struct sockaddr_in host_addr;
	int host_addrlen = sizeof(host_addr);
	host_addr.sin_family = AF_INET;
	host_addr.sin_port = htons(PORT);
	host_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    // Create client address
    struct sockaddr_in client_addr;
    int client_addrlen = sizeof(client_addr);

	if(bind(sockfd,(struct sockaddr *)&host_addr,host_addrlen)!=0)
	{
		perror("webserver (bind)");
		return 1;
	}
	printf("socket successfully bound to address\n");
	
	// Listen for incoming connections
	if(listen(sockfd,SOMAXCONN) != 0)
	{
		perror("webserver (listen)");
		return 1;
	}
	printf("server listening for connections on port %d\n",PORT);
    printc("#ff0000","#00ff00","test");	


	// accepting requests
	for(;;)
	{
		int newsockfd = accept(
				sockfd,
				(struct sockaddr *)&host_addr,
				(socklen_t *)&host_addrlen
				);

		if(newsockfd < 0)
		{
			perror("webserver (accept)");
			continue;
		}

		// Get client address
		int sockn = getsockname(newsockfd, (struct sockaddr *)&client_addr,(socklen_t *)&client_addrlen);
		if (sockn < 0) {
			perror("webserver (getsockname)");
			continue;
		}

		int valread = read(newsockfd,buffer,BUFFER_SIZE);
		if(valread < 0)
		{
			perror("webserver (read)");
			continue;
		}
		char method[BUFFER_SIZE], uri[BUFFER_SIZE], version[BUFFER_SIZE];
		sscanf(buffer, "%s %s %s", method, uri, version);
		time_t rawtime;
		struct tm * timeinfo;
		time(&rawtime);
		timeinfo = localtime(&rawtime);
		char *current_time = asctime(timeinfo);
		current_time[strlen(current_time)-1] = '\0';
		printf("[%s] @ %s:%u%s\n",current_time,inet_ntoa(client_addr.sin_addr),ntohs(client_addr.sin_port),uri);
		// if all has gone through then start setting up routes
		char *filename="server_c.html";
		FILE *fp = fopen(filename,"r");
		if(fp == NULL)
		{
			perror("webserver (html)");
			int response = write(newsockfd,"Internal Server Error",strlen("Internal Server Error"));
			if(response < 0)
			{
				perror("webserver (write)");
			}
		}

		// set up the default route

		if (strcmp(uri, "/") == 0) {
        		// Client has reached the home route
        		char content[BUFFER_SIZE * 2];  // Buffer to store full response
			char resp[] = "HTTP/1.0 200 OK\r\n"
                			"Server: webserver-c\r\n"
                			"Content-type: text/html\r\n\r\n";
		
        		memset(content, 0, sizeof(content));  // Clear the buffer

        		// Copy the HTTP header into the content
        		snprintf(content, sizeof(content), "%s", resp);

        		char buff[BUFFER_SIZE];

        		// Read the file content and append to the response
        		while (fgets(buff, sizeof(buff), fp) != NULL) {
        		// Append file content to the response
        		strncat(content, buff, sizeof(content) - strlen(content) - 1);
        		}

        		// Send the full response to the client
        		int response = write(newsockfd, content, strlen(content));
        		if (response < 0) {
        			perror("webserver (write)");
        		}
    		} else if(strcmp(uri,"/cat")==0)
		{
			serve_image(newsockfd,"/drive/.enc/decrypted/rou/cat.jpg");

		} else if (strcmp(uri,"/shutdown")==0){
			close(newsockfd);
			return 0;
		}
		fclose(fp);
		close(newsockfd);
	}
	return 0;
}
