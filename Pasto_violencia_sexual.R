library('ggplot2')
delitos.sexuales.2014 <- read.csv("~/Downloads/crimen2014/delitos-sexuales-2014.csv", sep=";")
datos_pasto <- subset(delitos.sexuales.2014, Municipio=='PASTO (CT)')
dias_semana <- data.frame("Dia" = c("Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"), "Numero_Delitos"=c(nrow(subset(datos_pasto, Día=='Lunes')),nrow(subset(datos_pasto, Día=='Martes')),nrow(subset(datos_pasto, Día=='Miércoles')),nrow(subset(datos_pasto, Día=='Jueves')),nrow(subset(datos_pasto, Día=='Viernes')),nrow(subset(datos_pasto, Día=='Sábado')),nrow(subset(datos_pasto, Día=='Domingo'))))
barrios <- data.frame('Barrio'=unique(datos_pasto$Barrio),'Numero_Delitos'=rep(0,57))
k=1
for(b in unique(datos_pasto$Barrio)){
  count <-nrow(subset(datos_pasto, Barrio==b))
  barrios[k,2] <- count
  k <- k+1
}
sexo <- data.frame('Sexo'=unique(datos_pasto$Sexo),'Numero_Delitos'=rep(0,3))
k=1
for(b in unique(datos_pasto$Sexo)){
  count <-nrow(subset(datos_pasto, Sexo==b))
  sexo[k,2] <- count
  k <- k+1
}
barplot(dias_semana$Numero_Delitos,names.arg = c('L','Ma','Mi','J','V','S','D'))
barplot(barrios$Numero_Delitos)
pie(sexo$Numero_Delitos,labels=sexo$Sexo)

escolaridad <- data.frame('Escolaridad'=unique(datos_pasto$Escolaridad),'Numero_Delitos'=rep(0,6))
k=1
for(b in unique(datos_pasto$Escolaridad)){
  count <-nrow(subset(datos_pasto, Escolaridad==b))
  escolaridad[k,2] <- count
  k <- k+1
}
barplot(escolaridad$Numero_Delitos,names.arg = c('Prim','Sec','?','Sup','Tec','-'))