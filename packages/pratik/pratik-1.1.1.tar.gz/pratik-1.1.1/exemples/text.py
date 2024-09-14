from pratik.text import Color, Highlight, Style, generate, information


def main():
    # Example of text colors
    print("Text colors with the Color class:")
    print(Color.RED + "Text in red" + Color.STOP)
    print(Color.GREEN + "Text in green" + Color.STOP)
    print(Color.BLUE + "Text in blue" + Color.STOP)

    # Example of custom RGB text colors
    print("\nText with RGB color using the Color class:")
    custom_color = Color(255, 105, 180)  # Hot pink
    print(custom_color.ansi_escape_sequence + "Text in hot pink" + Color.STOP)

    # Example of custom Hex text colors
    print("\nText with Hex color using the Color class:")
    hex_color = Color(hexadecimal="#ff6347")  # Tomato
    print(hex_color.ansi_escape_sequence + "Text in tomato" + Color.STOP)

    # Example of highlight colors for the background
    print("\nText with background highlight:")
    print(Highlight.RED + "Text with red background" + Highlight.STOP)
    print(Highlight.GREEN + "Text with green background" + Highlight.STOP)

    # Example of text styles
    print("\nText with various styles using the Style class:")
    print(Style.BOLD + "Bold text" + Style.NO_BOLD)
    print(Style.ITALIC + "Italic text" + Style.NO_ITALIC)
    print(Style.UNDERLINE + "Underlined text" + Style.NO_UNDERLINE)

    # Example of using the generate function
    print("\nText with generated ANSI sequences:")
    print(generate(31) + "Text in red (generated)" + generate(39))  # Red text and reset to default color
    print(
        generate(48, 2, 255, 105, 180) +
        "Text with hot pink background (generated)" +
        generate(49)
    )  # Hot pink background and reset to default background

    # Display ANSI code information
    print("\nANSI code table:")
    print(information())


if __name__ == "__main__":
    main()
