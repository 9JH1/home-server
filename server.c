//User friendly web server written in C
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <time.h>

#define PORT 6065
#define BUFFER_SIZE 1024

void serve_image(int client_socket, const char *image_path, int type) {
	FILE *image = fopen(image_path, "rb");
  if (!image) {
		printf("Error opening image file: %s\n", image_path);
		return;
  }
  fseek(image, 0, SEEK_END);
	long image_size = ftell(image);
	fseek(image, 0, SEEK_SET);
  char *image_buffer = (char *)malloc(image_size);
  fread(image_buffer, 1, image_size, image);
	const char *http_header = "HTTP/1.1 200 OK\r\n";
  const char *content_type_header = "Content-Type: image/jpeg\r\n";
  const char *connection_header = "Connection: close\r\n";
  write(client_socket, http_header, strlen(http_header));
  write(client_socket, content_type_header, strlen(content_type_header));
  write(client_socket, connection_header, strlen(connection_header));
  write(client_socket, "\r\n", 2); // End of headers
  write(client_socket, image_buffer, image_size);
  free(image_buffer);
  fclose(image);
}

int main(){
	char buffer[BUFFER_SIZE];

	// Create a socket
	int sockfd = socket(AF_INET,SOCK_STREAM,0);
	if(sockfd == -1) return 1; //TODO: fix this bs
	else { /* socket created successfully */}
	struct sockaddr_in host_addr;
	int host_addrlen = sizeof(host_addr);
	host_addr.sin_family = AF_INET;
	host_addr.sin_port = htons(PORT);
	host_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  struct sockaddr_in client_addr;
  int client_addrlen = sizeof(client_addr);
	if(bind(sockfd,(struct sockaddr *)&host_addr,host_addrlen)!=0) return 1;
	printf("socket successfully bound to address\n");
	if(listen(sockfd,SOMAXCONN) != 0) return 1;
	printf("server listening for connections on port %d\n",PORT);
	for(;;){
		int newsockfd = accept(sockfd,(struct sockaddr *)&host_addr,(socklen_t *)&host_addrlen);
		if(newsockfd < 0) continue;
		int sockn = getsockname(newsockfd, (struct sockaddr *)&client_addr,(socklen_t *)&client_addrlen);
		if (sockn < 0) continue;
		int valread = read(newsockfd,buffer,BUFFER_SIZE);
		if(valread < 0){continue;}
		char method[BUFFER_SIZE], uri[BUFFER_SIZE], version[BUFFER_SIZE];
		sscanf(buffer, "%s %s %s", method, uri, version);
		time_t rawtime;
		struct tm * timeinfo;
		time(&rawtime);
		timeinfo = localtime(&rawtime);
		char *current_time = asctime(timeinfo);
		current_time[strlen(current_time)-1] = '\0';
		printf("[%s] @ %s:%u%s\n",current_time,inet_ntoa(client_addr.sin_addr),ntohs(client_addr.sin_port),uri);
		char *filename="server_c.html";
		FILE *fp = fopen(filename,"r");
		if(fp == NULL){
			perror("webserver (html)");
			int response = write(newsockfd,"Internal Server Error",strlen("Internal Server Error"));
			if(response < 0) perror("webserver (write)");
		}

		// start comparisons
		if (strcmp(uri, "/") == 0) {
      char content[BUFFER_SIZE * 2];
			char resp[] = "HTTP/1.0 200 OK\r\n" "Server: webserver-c\r\n" "Content-type: text/html\r\n\r\n";
      memset(content, 0, sizeof(content));
      snprintf(content, sizeof(content), "%s", resp);
      char buff[BUFFER_SIZE];
      while (fgets(buff, sizeof(buff), fp) != NULL) strncat(content, buff, sizeof(content) - strlen(content) - 1);
      int response = 0;
			response = write(newsockfd, content, strlen(content));
      if (response < 0) {/* just another write error */}
		}
		fclose(fp);
		close(newsockfd);
	}
	return 0;
}
