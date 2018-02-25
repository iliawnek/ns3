#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netdb.h>

int main(int argc, char *argv[]) {
  // exit if domain names are not given
	if (argc < 2) return -1;
  
  // iterate through each given domain name
  for (int i = 1; i < argc; i++) {
    char *domain_name = argv[i];
    struct addrinfo hints;
    struct addrinfo *ai0;
    struct addrinfo *ai;
    int i;
    char ip_address[INET6_ADDRSTRLEN];
    
    // get IP address information corresponding to domain name
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = PF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
  	if ((i = getaddrinfo(domain_name, "80", &hints, &ai0)) != 0) continue;
  	
    // print IP addresses
  	for (ai = ai0; ai != NULL; ai = ai->ai_next) {
      if (ai->ai_family == AF_INET) { // IPv4
        if (inet_ntop(AF_INET, &((struct sockaddr_in *) ai->ai_addr)->sin_addr, ip_address, sizeof(ip_address)) == NULL) continue;
        printf("%s IPv4 %s\n", domain_name, ip_address);
      } else if (ai->ai_family == AF_INET6) { // IPv6
        if (inet_ntop(AF_INET6, &((struct sockaddr_in6 *) ai->ai_addr)->sin6_addr, ip_address, sizeof(ip_address)) == NULL) continue;
        printf("%s IPv6 %s\n", domain_name, ip_address);
  		}
  	}
  }
}
