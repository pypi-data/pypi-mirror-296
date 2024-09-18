import main, pygame

screen = pygame.display.set_mode()

main.setComponents("components.json")
menu = main.Page(screen, "page.json")

run = True
while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(main.convertColor("f"))

    menu.show()
    pygame.display.flip()