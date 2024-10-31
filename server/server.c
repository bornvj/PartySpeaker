#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/stat.h>

#define PORT 80
#define BUFFER_SIZE 4096

// Default error handler
void error(const char *msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}

// Decode un URL vers une string utilisable
void decode_url(const char *src, char *dest) {
    while (*src) {
        if (*src == '%') {
            int value;
            sscanf(src + 1, "%2x", &value);
            *dest++ = (char)value;
            src += 3;
        } else if (*src == '+') {
            *dest++ = ' ';
            src++;
        } else {
            *dest++ = *src++;
        }
    }
    *dest = '\0';
}

// Envoie une reponse
void send_response(int client_socket, const char *status, const char *content_type, const char *body) {
    char response[BUFFER_SIZE];
    snprintf(response, sizeof(response),
             "HTTP/1.1 %s\r\n"
             "Content-Type: %s\r\n"
             "Content-Length: %zu\r\n"
             "\r\n"
             "%s", status, content_type, strlen(body), body);
    send(client_socket, response, strlen(response), 0);
}

// Envoie la page HTML pageName
void serve_index(int client_socket, char* pageName) {
    FILE *fp = fopen(pageName, "r");
    if (fp == NULL) {
        send_response(client_socket, "500 Internal Server Error", "text/plain", "Failed to open HTML file");
        return;
    }

    char html[BUFFER_SIZE];
    memset(html, 0, sizeof(html));
    fread(html, sizeof(char), sizeof(html) - 1, fp);
    if (strcmp(pageName, "server/source/index.html") == 0)
    {
        // customiser la page HTML si c'est l'index
        char saveHtml[BUFFER_SIZE];

        char* ptr = strstr(html, "-->");
        ptr += strlen("-->\n");
        strcpy(saveHtml, ptr);
        ptr++;
        *ptr = '\0';

        //char* stringToInsert = "<h4>Je suis une ligne du fichier\nEt moi une autre\n</h4>";
        //strcat(ptr, stringToInsert);

        char* count = getenv("LINECOUNT");
        if(count)
            printf("%s\n", count);
        else
            printf("pas de varriable env\n");

        FILE *tracks = fopen("soundQueue/titles.txt", "r");

        char line[BUFFER_SIZE];
        memset(line, 0, sizeof(line));
        while (fgets(line, sizeof(line), tracks)) {
            strcat(ptr, "<h4>");
            strcat(ptr, line); // Ajouter la ligne au contenu
            strcat(ptr, "</h4>\n");
        }
        fclose(tracks);

    }
    html[sizeof(html) - 1] = '\0'; // Assurez-vous que le buffer est null-terminé
    fclose(fp);

    send_response(client_socket, "200 OK", "text/html", html);
}

void handle_upload(int client_socket, const char *body) {
    // Enregistrer le texte dans un fichier
    FILE *fp = fopen("soundQueue/queue.txt", "a");
    if (fp == NULL) {
        send_response(client_socket, "500 Internal Server Error", "text/plain", "Failed to open file");
        return;
    }

    const char* text = body + strlen("text="); // avoir le pointeur vers le text sans 'text='
    char* decodedText = malloc(strlen(text) + 1);

    decode_url(text, decodedText);

    printf("Received decode: [%s]\n", decodedText);
    char* end = "\n";

    fwrite(decodedText, sizeof(char), strlen(decodedText),  fp);
    fwrite(end, sizeof(char), strlen(end),  fp);
    fclose(fp);

    free(decodedText);

    serve_index(client_socket, "server/source/uploadDone.html");
}


void handle_request(int client_socket) {
    char buffer[BUFFER_SIZE];
    memset(buffer, 0, sizeof(buffer));
    recv(client_socket, buffer, sizeof(buffer) - 1, 0);
    buffer[sizeof(buffer) - 1] = '\0'; //  null-terminé

    // GET /
    if (strstr(buffer, "GET / ") != NULL)
    {
        serve_index(client_socket, "server/source/index.html"); // envoie la racine
        return;
    }

    // GET /upload
    if (strstr(buffer, "GET /upload ") != NULL)
    {
        serve_index(client_socket, "server/source/upload.html"); // envoie le lien pour rediriger a la racine
        return;
    }

    if (strstr(buffer, "POST /upload") != NULL) {
        char *content_start = strstr(buffer, "\r\n\r\n");

        if (content_start) {
            content_start += 4; // Skip \r\n\r\n

            handle_upload(client_socket, content_start);
        } else {
            send_response(client_socket, "400 Bad Request", "text/plain", "Invalid request");
        }
        return;
    }
}

int create_file(const char* path)
{
    FILE *fp = fopen(path, "w");
    fclose(fp);
    chmod(path, 0777);
    return 0;
}

int main() {
    // Recrée queue.txt et titles.txt
    create_file("soundQueue/queue.txt");
    create_file("soundQueue/titles.txt");

    int server_fd, client_socket;
    struct sockaddr_in address;
    int opt = 1;
    socklen_t addrlen = sizeof(address);

    // Création du socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
        error("socket failed");

    // Attacher le socket au port
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)))
        error("setsockopt");

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Lier le socket
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
        error("bind failed");

    // Écouter les connexions entrantes
    if (listen(server_fd, 3) < 0)
        error("listen");

    printf("Serveur HTTP en attente de connexions sur le port %d...\n", PORT);

    while (1) {
        // Accepter une connexion
        if ((client_socket = accept(server_fd, (struct sockaddr *)&address, &addrlen)) < 0) {
            error("accept");
        }

        handle_request(client_socket);
        close(client_socket);
    }

    close(server_fd);
    return 0;
}
