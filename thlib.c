#include <stdio.h>
#include <string.h>
#include <stdlib.h>


void htr(const char *hex, int *r, int *g, int *b)
{
    // Ensure the hex string is valid
    if (hex[0] != '#' || strlen(hex) != 7)
    {
        fprintf(stderr, "Invalid hex color code.\n");
        exit(1);
    }
    // Convert the hex string to RGB values
    *r = (int)strtol(hex + 1, NULL, 16) >> 16;
    *g = ((int)strtol(hex + 1, NULL, 16) >> 8) & 0xFF;
    *b = (int)strtol(hex + 1, NULL, 16) & 0xFF;
}
void printc(const char *fg_hex, const char *bg_hex, const char *text)
{
    if (fg_hex == NULL && bg_hex == NULL)
    {
        printf("%s", text);
        return;
    }
    int foreground_r, foreground_g, foreground_b;
    int background_r, background_g, background_b;
    char escape_seq[128] = "\033["; // Buffer to build the escape sequence
    int first = 1;

    // Initialize escape sequence buffer
    escape_seq[0] = '\033';
    escape_seq[1] = '[';
    escape_seq[2] = '\0';

    // Convert and apply foreground color if provided

    if (fg_hex != NULL || fg_hex != "")
    {
        htr(fg_hex, &foreground_r, &foreground_g, &foreground_b);
        if (!first)
        {
            strcat(escape_seq, ";");
        }
        strcat(escape_seq, "38;2;");
        char temp[32];
        snprintf(temp, sizeof(temp), "%d;%d;%d", foreground_r, foreground_g, foreground_b);
        strcat(escape_seq, temp);
        first = 0;
    }

    // Convert and apply background color if provided
    if (bg_hex != NULL || bg_hex != "")
    {
        if (!first)
        {
            strcat(escape_seq, ";");
        }
        strcat(escape_seq, "48;2;");
        htr(bg_hex, &background_r, &background_g, &background_b);
        char temp[32];
        snprintf(temp, sizeof(temp), "%d;%d;%d", background_r, background_g, background_b);
        strcat(escape_seq, temp);
    }

    // Finalize the escape sequence and print
    if (strlen(escape_seq) > 2)
    {
        strcat(escape_seq, "m");
        printf("%s%s\033[0m", escape_seq, text);
    }
    else
    {
        // No color escape sequence, just print text normally
        printf("%s\033[0m", text);
    }
}
