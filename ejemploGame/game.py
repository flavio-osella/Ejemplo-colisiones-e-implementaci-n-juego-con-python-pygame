import pygame



class Protagonista(pygame.sprite.Sprite):
    cambio_x = 0
    cambio_y = 0
    aLaIzq= False
    aLaDer= False
    nivel=None
    bichos=None
    
 
    def __init__(self,x,y):
        super().__init__()
        self.sheet = pygame.image.load('imagenes/kate.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(0, 0, 45, 70))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
        self.frame = 0
        self.left_states = { 0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76) }
        self.right_states = { 0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76) }
        self.saltoLeft_states= { 0:(0, 76, 52, 76)}
        self.saltoRight_states={0:(0, 152, 52, 76)}

    def get_frame(self, frame_set):     #loop que repite los frames que definimos arriba 
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):  #lo mismo ejecuta el loop pero con los recortes de los rect
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def calc_grav(self):
        """ Calculamos el efecto de la gravedad. """
        if self.cambio_y == 0:
            self.cambio_y = 15
        else:
            self.cambio_y += .25

        if self.rect.y >= 450 and self.cambio_y >= 0:
            self.cambio_y = 0
            self.rect.y = 450

    def saltar(self):        # Si está listo para saltar, aumentamos nuestra velocidad hacia arriba
        
        self.rect.y += 2
        lista_impactos_plataforma = pygame.sprite.spritecollide(self, self.nivel.listade_sprites, False,pygame.sprite.collide_rect)
        self.rect.y -= 2

        if len(lista_impactos_plataforma) > 0 or self.rect.bottom >= 450:
            self.cambio_y = -18        

    def update(self,cosas,enemigos):

        self.calc_grav()        

        self.rect.x += self.cambio_x                 
        lista_impactos_bloques = cosas
        for bloque in cosas :            
            if pygame.sprite.collide_rect(self,bloque) :
                if self.aLaDer== True and self.rect.right > bloque.rect.left :
                    self.rect.right = bloque.rect.left                           
                if self.aLaIzq == True and self.rect.left < bloque.rect.right :                
                    self.rect.left= bloque.rect.right                 
        self.rect.y += self.cambio_y        
        lista_impactos_bloques = cosas
        for bloque in cosas :            
            if pygame.sprite.collide_rect(self,bloque):
                if  self.cambio_y > 0:
                    self.rect.bottom = bloque.rect.top                         
                elif  self.cambio_y < 0:
                    self.rect.top = bloque.rect.bottom
                self.cambio_y = 0       
        
        lista_impactos_enemigos= enemigos
        for enemigo in enemigos :
            if pygame.sprite.collide_rect(self,enemigo):
                if self.aLaDer== True and self.rect.right > enemigo.rect.left :
                    self.rect.right = enemigo.rect.left                           
                if self.aLaIzq == True and self.rect.left < enemigo.rect.right :                
                    self.rect.left= enemigo.rect.right     
                elif self.cambio_y > 0:
                    self.rect.bottom = enemigo.rect.top
                elif self.cambio_y < 0 :
                    self.rect.top = enemigo.rect.bottom        

    def mover(self,direction):

        if direction == 'left':
            self.clip(self.left_states)
            self.rect.x -= 18
            self.aLaIzq= True
            self.aLaDer= False
        if direction == 'right':
            self.clip(self.right_states)
            self.rect.x += 18
            self.aLaDer= True
            self.aLaIzq= False
        if direction == 'stand_left':
            self.clip(self.left_states[0])
            self.aLaIzq= True
            self.aLaDer= False
        if direction == 'stand_right':
            self.clip(self.right_states[0])
            self.aLaDer= True
            self.aLaIzq= False
        if direction == 'up':
            if self.aLaIzq == True :
                self.clip(self.saltoLeft_states)
                self.saltar()             
            if self.aLaDer == True  :
                self.clip(self.saltoRight_states)
                self.saltar()                      
        if direction=='stand_up': 
            if self.aLaIzq == True :
                self.cambio_y=0
                self.saltoLeft_states[0]                
            if self.aLaDer == True  :
                self.cambio_y=0
                self.saltoRight_states[0]            
        
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.mover('left')
            if event.key == pygame.K_RIGHT:
                self.mover('right')
            if event.key == pygame.K_UP:
                self.mover('up')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.mover('stand_left')
            if event.key == pygame.K_RIGHT:
                self.mover('stand_right')
            if event.key == pygame.K_UP:
                self.mover('stand_up')

class Bicho(pygame.sprite.Sprite):    
        cambio_x = 15
        cambio_y = 8 
        nivel=None
        bichos=None       
        
        def __init__(self,x,y):
            super().__init__()
            self.image_1= pygame.image.load('imagenes/cosa1.png')
            self.image_2= pygame.image.load('imagenes/cosa2.png')
            self.image_3= pygame.image.load('imagenes/cosa3.png')
            self.listaImagenes= [self.image_1,self.image_2,self.image_3]
            self.posImage = 0
            self.image = self.listaImagenes[self.posImage]
            self.rect= self.image.get_rect()
            self.rect.x= x
            self.rect.y= y         

        def comportamiento(self):                
            self.posImage += 1           
            if self.posImage > len(self.listaImagenes) - 1:
                self.posImage = 0

        def volar(self):
            self.comportamiento()
            self.image= self.listaImagenes[self.posImage]
                    
        def update(self):            
            self.rect.x += self.cambio_x
            self.rect.y += self.cambio_y
            self.volar()                     
            if self.rect.x > 600  :            
                self.cambio_x= self.cambio_x * -1                
                self.volar()                         
            if self.rect.x < 60  :              
                self.cambio_x = self.cambio_x * -1
                self.volar()
            if self.rect.y < 100:
                self.cambio_y= self.cambio_y * -1
                self.volar()
            if self.rect.y > 200 :
                self.cambio_y= self.cambio_y * -1
                self.volar ()
            self.rect.topleft= (self.rect.x , self.rect.y )

class Bicho2(pygame.sprite.Sprite):    
        cambio_x = 15
        cambio_y = 8 
        nivel=None
        bichos=None       
        
        def __init__(self,x,y):
            super().__init__()
            self.image_1= pygame.image.load('imagenes/coso1.png')
            self.image_2= pygame.image.load('imagenes/coso2.png')
            self.image_3= pygame.image.load('imagenes/coso3.png')
            self.image_4= pygame.image.load('imagenes/coso4.png')
            self.image_5= pygame.image.load('imagenes/coso7.png')
            self.image_6= pygame.image.load('imagenes/coso8.png')
            self.image_7= pygame.image.load('imagenes/coso9.png')
            self.image_8= pygame.image.load('imagenes/coso10.png')
            self.listaImagenes= [self.image_1,self.image_2,self.image_3,self.image_4]
            self.listaImagenes2= [self.image_5,self.image_6,self.image_7,self.image_8]
            self.todasImagenes= [self.listaImagenes,self.listaImagenes2]
            self.posImage = 0
            self.variable= 0
            self.izquierda = False
            self.paraArriba= False
            self.image =self.todasImagenes[self.variable][self.posImage]
            self.image.set_clip(pygame.Rect(0, 0,64, 64))
            self.image = self.image.subsurface(self.image.get_clip())      
            self.rect= self.image.get_rect()              
            self.x= x
            self.y= y        

        def comportamiento(self):                
            self.posImage += 1 
            self.variable= 0          
            if self.posImage > len(self.todasImagenes[self.variable]) - 1:
                self.posImage = 0

        def comportamiento2(self):
            self.posImage +=1
            self.variable= 1
            if self.posImage > len(self.todasImagenes[self.variable])-1:
                self.posImage = 0
        
        def volar(self):
            if  not self.izquierda :                       
                self.comportamiento()
                self.image = self.todasImagenes[self.variable][self.posImage]
            else:              
                self.comportamiento2()
                self.image = self.todasImagenes[self.variable][self.posImage]
            
            
        def update(self):
            self.rect.x += self.cambio_x
            self.rect.y += self.cambio_y
            self.volar()
            if self.rect.x > 600:
                self.izquierda= True 
                self.cambio_x = self.cambio_x * -1
                self.volar()
            elif self.rect.x < 60 :
                self.izquierda= False
                self.cambio_x = self.cambio_x * -1
                self.volar()
            elif self.rect.y < 100 and self.paraArriba== True:
                self.paraArriba= False
                self.cambio_y= self.cambio_y * -1
                self.volar()
            elif self.rect.y > 200 and self.paraArriba==False :
                self.paraArriba= True
                self.cambio_y= self.cambio_y * -1
                self.volar ()
            
        
                

                 
class Lizard(pygame.sprite.Sprite):
    nivel=None
    bichos=None
    cambio_x = 10        
    
    def __init__(self,x,y):
        super().__init__()
        self.image_1= pygame.image.load('imagenes/lizard1.png')
        self.image_2= pygame.image.load('imagenes/lizard2.png')
        self.image_3= pygame.image.load('imagenes/lizard3.png')
        self.image_4= pygame.image.load('imagenes/lizard4.png')
        self.image_5= pygame.image.load('imagenes/lizard5.png')
        self.image_6= pygame.image.load('imagenes/lizard6.png')
        self.image_7= pygame.image.load('imagenes/lizard7.png')
        self.image_8= pygame.image.load('imagenes/lizard8.png')
        self.image_9= pygame.image.load('imagenes/lizard9.png')
        self.image_10=pygame.image.load('imagenes/lizard10.png')
        self.image_11=pygame.image.load('imagenes/lizard11.png')
        self.image_12=pygame.image.load('imagenes/lizard12.png')
        self.image_13=pygame.image.load('imagenes/lizard13.png')
        self.image_14=pygame.image.load('imagenes/lizard14.png')
        self.image_15=pygame.image.load('imagenes/lizard15.png')
        self.image_16=pygame.image.load('imagenes/lizard16.png')
        self.image_17=pygame.image.load('imagenes/lizard17.png')
        self.image_18=pygame.image.load('imagenes/lizard18.png')
        self.image_19=pygame.image.load('imagenes/lizard19.png')    
        self.listaImagenes= [self.image_1,self.image_2,self.image_3,self.image_4,self.image_5,self.image_6,self.image_7,self.image_8,self.image_9,self.image_10]
        self.listaImagenes2= [self.image_11,self.image_12,self.image_13,self.image_14,self.image_15,self.image_16,self.image_17,self.image_18,self.image_19]
        self.todasImagenes= [self.listaImagenes,self.listaImagenes2]
        self.posImage = 0
        self.variable= 0
        self.izquierda = False
        self.image =self.todasImagenes[self.variable][self.posImage]
        self.image.set_clip(pygame.Rect(0, 0,150, 150))
        self.image = self.image.subsurface(self.image.get_clip())      
        self.rect= self.image.get_rect()              
        self.x= x
        self.y= y        

    def comportamiento(self):                
        self.posImage += 1 
        self.variable= 0          
        if self.posImage > len(self.todasImagenes[self.variable]) - 1:
            self.posImage = 0

    def comportamiento2(self):
        self.posImage +=1
        self.variable= 1
        if self.posImage > len(self.todasImagenes[self.variable])-1:
            self.posImage = 0
        
    def caminar(self):
        if  not self.izquierda :                       
            self.comportamiento()
            self.image = self.todasImagenes[self.variable][self.posImage]
        else:              
            self.comportamiento2()
            self.image = self.todasImagenes[self.variable][self.posImage]
            
    def update(self):
        self.rect.x += self.cambio_x
        self.caminar()
        if self.rect.x > 600:
            self.izquierda= True 
            self.cambio_x = self.cambio_x * -1
            self.caminar()
        elif self.rect.x < 60 :
            self.izquierda= False
            self.cambio_x = self.cambio_x * -1
            self.caminar()
        

class Rana(pygame.sprite.Sprite):
    cambio_x = 0        
    nivel=None
    nivel2=None

    def __init__(self,x,y):
        super().__init__()
        self.image_1= pygame.image.load('imagenes/1.png')
        self.image_2= pygame.image.load('imagenes/2.png')
        self.image_3= pygame.image.load('imagenes/3.png')
        self.image_4= pygame.image.load('imagenes/4.png')
        self.image_5= pygame.image.load('imagenes/5.png')
        self.image_6= pygame.image.load('imagenes/6.png')
        self.image_7= pygame.image.load('imagenes/7.png')
        self.image_8= pygame.image.load('imagenes/8.png')
        self.image_9= pygame.image.load('imagenes/9.png')
        self.image_10=pygame.image.load('imagenes/10.png')
        self.image_11=pygame.image.load('imagenes/11.png')
        self.image_12=pygame.image.load('imagenes/12.png')
        self.image_13=pygame.image.load('imagenes/13.png')
        self.image_14=pygame.image.load('imagenes/14.png')
        self.image_15=pygame.image.load('imagenes/15.png')
        self.image_16=pygame.image.load('imagenes/16.png')
        self.image_17=pygame.image.load('imagenes/17.png')
        self.image_18=pygame.image.load('imagenes/18.png')
        self.image_19=pygame.image.load('imagenes/19.png')
        self.image_20=pygame.image.load('imagenes/20.png') 
        self.image_21=pygame.image.load('imagenes/21.png')
        self.image_22=pygame.image.load('imagenes/22.png')
        self.image_23=pygame.image.load('imagenes/23.png')
        self.image_24=pygame.image.load('imagenes/24.png')
        self.image_25=pygame.image.load('imagenes/25.png')
        self.image_26=pygame.image.load('imagenes/26.png')
        self.image_27=pygame.image.load('imagenes/27.png')
        self.image_28=pygame.image.load('imagenes/28.png')
        self.image_29=pygame.image.load('imagenes/29.png')
        self.image_30=pygame.image.load('imagenes/30.png')
        self.image_31=pygame.image.load('imagenes/31.png')
        self.image_32=pygame.image.load('imagenes/32.png') 
        self.listaImagenes= [self.image_1,self.image_2,self.image_3,self.image_4,self.image_5,self.image_6,self.image_7,self.image_8,self.image_9,self.image_10,self.image_11,self.image_12,self.image_13,self.image_14,self.image_15,self.image_16,
                             self.image_17,self.image_18,self.image_19,self.image_20,self.image_21,self.image_22,self.image_23,self.image_24,self.image_25,self.image_26,self.image_27,self.image_28,self.image_29,self.image_30,self.image_31,self.image_32]
        self.posImage = 0
        self.izquierda = False
        self.image =self.listaImagenes[self.posImage]       
        self.rect= self.image.get_rect()        
        self.rect.x= x
        self.rect.y= y        

    def comportamiento(self):                
        self.posImage += 1         
        if self.posImage > len(self.listaImagenes) - 1:
            self.posImage = 0
      
            
    def update(self):
        self.rect.x += self.cambio_x
        self.comportamiento()
        self.image = self.listaImagenes[self.posImage]
      
            
          
class Plataforma(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('imagenes/plataforma2.png').convert_alpha()
        self.image.set_clip(pygame.Rect(0, 0,200, 50))
        self.image = self.image.subsurface(self.image.get_clip())
        self.rect = self.image.get_rect()   
        self.rect.y = y
        self.rect.x = x
        self.rect.topleft= self.rect.x , self.rect.y

class Hongo(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("imagenes/hongo.png").convert_alpha()
        self.image.set_clip(pygame.Rect(0,0,81,85))
        self.image= self.image.subsurface(self.image.get_clip())
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.rect.topleft= self.rect.x , self.rect.y


class Nivel(object):
    
    def __init__(self, protagonista):        
        self.listade_sprites = pygame.sprite.Group()
        self.listade_enemigos= pygame.sprite.Group()
        self.protagonista = protagonista

    def update(self):        
        self.listade_sprites.update()
        self.listade_enemigos.update()

    def draw(self, pantalla):       
        self.listade_sprites.draw(pantalla)
        self.listade_enemigos.draw(pantalla)

class Nivel_1(Nivel):
    def __init__(self,protagonista):
        Nivel.__init__(self,protagonista)
        
        nivel=[[100,300],[400,250],[350,150]]
        bichos=[[100,100],[200,300]]
        hongos= [[450,450]]

        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.protagonista = self.protagonista
            self.listade_sprites.add(bloque)

        for bicho in bichos:
            cosa = Bicho(bicho[0], bicho[1])
            cosa.rect.x = bicho[0]
            cosa.rect.y = bicho[1]
            cosa.protagonista = self.protagonista
            self.listade_enemigos.add(cosa)

        for hongo in hongos:
            cosa = Hongo(hongo[0], hongo[1])
            cosa.rect.x = hongo[0]
            cosa.rect.y = hongo[1]
            cosa.protagonista = self.protagonista
            self.listade_sprites.add(cosa)
         

class Nivel_2(Nivel):
    def __init__(self,protagonista):
        Nivel.__init__(self,protagonista)
        
        nivel=[[150,300],[350,250]]

        bichos=[[100,100]]

        

        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.protagonista = self.protagonista
            self.listade_sprites.add(bloque) 
            
        for bicho in bichos:
            cosa = Bicho2(bicho[0], bicho[1])
            cosa.rect.x = bicho[0]
            cosa.rect.y = bicho[1]
            cosa.protagonista = self.protagonista
            self.listade_enemigos.add(cosa)

 #       for rana in ranas:
 #           ran= Rana(rana[0],rana[1])
 #           ran.rect.x= rana[0]
 #           ran.rect.y= rana[1]
 #           ran.protagonista= self.protagonista
 #           self.listade_sprites.add(ran)
       
              

class Nivel_3(Nivel):
    def __init__(self,protagonista):
        Nivel.__init__(self,protagonista)
        
        nivel=[[150,300],[250,250],[450,150]]

        bichos=[[60,350]]

        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.protagonista = self.protagonista
            self.listade_sprites.add(bloque)
      
        for bicho in bichos:
            cosa = Lizard(bicho[0], bicho[1])
            cosa.rect.x = bicho[0]
            cosa.rect.y = bicho[1]
            cosa.protagonista = self.protagonista
            self.listade_enemigos.add(cosa)

class Nivel_4(Nivel):
    def __init__(self,protagonista):
        Nivel.__init__(self,protagonista)


        
        


def main():

    pygame.init()

    dimensiones= [950,550]
    pantalla= pygame.display.set_mode(dimensiones)    
    pygame.display.set_caption('Kate Game')

    protagonista= Protagonista(60,450)

    listade_niveles = []
    listade_niveles.append(Nivel_1(protagonista))
    listade_niveles.append(Nivel_2(protagonista))
    listade_niveles.append(Nivel_3(protagonista))
    listade_niveles.append(Nivel_4(protagonista))
     
    # Establecemos el nivel actual
    nivel_actual_no = 0
    nivel_actual = listade_niveles[nivel_actual_no]
     
    lista_sprites_activos = pygame.sprite.Group()
    lista_sprites_activos.add(protagonista)
    protagonista.nivel = nivel_actual
    
    reloj= pygame.time.Clock()

    hecho= False
    
    while not hecho:          #Bucle principal del juego.

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
        protagonista.handle_event(evento)

        protagonista.update(nivel_actual.listade_sprites, nivel_actual.listade_enemigos)

        if protagonista.rect.x <= 0 :
            if nivel_actual_no == 0:
                protagonista.cambio_x= 0                          
            elif nivel_actual_no == 1:
                nivel_actual_no= 0
                nivel_actual= listade_niveles[nivel_actual_no]
                protagonista.rect.x= 940                
            elif nivel_actual_no==2:
                nivel_actual_no=1
                nivel_actual= listade_niveles[nivel_actual_no]
                protagonista.rect.x= 940
                nivel_actual.update()
            elif nivel_actual_no==3:
                nivel_actual_no=2
                nivel_actual= listade_niveles[nivel_actual_no]
                protagonista.rect.x= 940
        elif protagonista.rect.x >= 951:
            if nivel_actual_no== 0:
                nivel_actual_no= 1
                nivel_actual= listade_niveles[nivel_actual_no]                
                protagonista.rect.x= 0                
            elif nivel_actual_no== 1:
                nivel_actual_no= 2
                nivel_actual= listade_niveles[nivel_actual_no]
                protagonista.rect.x= 0
            elif nivel_actual_no==2:
                nivel_actual_no= 3
                nivel_actual= listade_niveles[nivel_actual_no]
                protagonista.rect.x= 0 
                        
        elif nivel_actual_no==0:
            fondo= pygame.image.load("imagenes/fondo2.png").convert()
            pantalla.blit(fondo, [0, 0])
        elif nivel_actual_no==1:
            fondo= pygame.image.load("imagenes/fondo2.png").convert()
            pantalla.blit(fondo, [0, 0])
        elif nivel_actual_no==2:
            fondo= pygame.image.load("imagenes/fondo3.png").convert()
            pantalla.blit(fondo, [0,0])
        elif nivel_actual_no==3:
            fondo= pygame.image.load("imagenes/fondo4.png").convert()
            pantalla.blit(fondo, [0,0])

        nivel_actual.update()
        nivel_actual.draw(pantalla)
        lista_sprites_activos.draw(pantalla)
        reloj.tick(60)
        pygame.display.flip()
        
    pygame.quit()

if __name__== "__main__":
    main()








        



























