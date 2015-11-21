-- SALA DE CINE

CREATE TABLE peliculas (
    codigo int PRIMARY KEY
    ,nombre varchar(100)
    ,CalificacionEdad int
    );
    
CREATE TABLE salas (
    codigo int PRIMARY KEY
    ,nombre varchar(100)
    ,pelicula int
    ,FOREIGN KEY (pelicula) REFERENCES peliculas (codigo)
    );

-- FABRICANTES

CREATE TABLE fabricantes (
    codigo int
    ,nombre varchar(100)
    ,PRIMARY KEY codigo
)

CREATE TABLE articulos (
    codigo int
    ,nombre varchar(100)
    ,precio int
    ,fabricante int
    ,FOREIGN KEY (fabricante) REFERENCES fabricantes (codigo)
    );
    

    /*
CREATE TABLE articulos (
    codigo int PRIMARY KEY
    ,nombre varchar(100)
    ,precio int
    ,fabricante int REFERENCES fabricantes (codigo)
    );
    */
    
    
    
-- Grandes Almacenes
CREATE TABLE cajeros (
    codigo int PRIMARY KEY
    ,NomApels varchar(255)
    );
    
CREATE TABLE maquinas_registradoras (
    codigo int PRIMARY KEY
    ,Piso int
    );
    
CREATE TABLE productos (
    codigo int PRIMARY KEY
    ,Nombre varchar(100)
    ,Precio int
    );
    
CREATE TABLE venta (
    Cajero int
    ,Maquina int
    ,Producto int
    ,PRIMARY KEY (Cajero,Maquina,Producto)
    ,FOREING KEY (Cajero) REFERENCES cajeros (codigo)...
    ....
)
    