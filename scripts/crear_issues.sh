#!/usr/bin/env bash
# Crea etiquetas e issues iniciales con GitHub CLI (gh). Ejecutar UNA vez dentro del repo ya subido.
# Requisitos: gh instalado y autenticado (gh auth login).
# Uso: bash scripts/crear_issues.sh USUARIO_CRISTIAN USUARIO_PABLO
set -e
CRISTIAN="${1:?Falta usuario GitHub de Cristian}"
PABLO="${2:?Falta usuario GitHub de Pablo}"

gh label create parte-cristian --color 1D76DB --force
gh label create parte-pablo --color 0E8A16 --force
gh label create bug --color D73A4A --force
gh label create docs --color 0075CA --force
gh label create bloqueante --color B60205 --force
gh label create integracion --color 5319E7 --force

crear() { gh issue create --title "$1" --body "$2" --label "$3" --assignee "$4"; }

crear "C1: Entorno y documentación de instalación" "Probar README/.env.example en máquina limpia." parte-cristian "$CRISTIAN"
crear "C2: Afinar modelos Genero y Espectaculo" "Validadores, PROTECT, choices, ImageField, baja lógica; migraciones limpias." parte-cristian "$CRISTIAN"
crear "C3: Validators y QuerySet (vigentes/disponibles)" "Contrato con Pablo y reservas." parte-cristian "$CRISTIAN"
crear "C4: Comando poblar_datos" "4+ géneros, 8+ espectáculos, usuarios admin y cliente; idempotente; --limpiar." parte-cristian "$CRISTIAN"
crear "C5: Admin corporativo (títulos)" "site_header, site_title, index_title." parte-cristian "$CRISTIAN"
crear "C6: ModelAdmin avanzado" "list_display, list_filter, search_fields, list_editable, fieldsets." parte-cristian "$CRISTIAN"
crear "C7: Clase Carrito (sesión)" "Interfaz de reservas/carrito.py + tests." parte-cristian "$CRISTIAN"
crear "C8: Vistas y plantillas de reservas" "Ver, agregar, modificar, eliminar, vaciar, confirmar, comprobante." parte-cristian "$CRISTIAN"
crear "C9: Context processor del contador" "Contador en navbar en todas las páginas." parte-cristian "$CRISTIAN"
crear "C10: Pruebas de modelos, comando y carrito" "Cobertura de casos felices y de error." parte-cristian "$CRISTIAN"
crear "C11: Documentación y bitácora IA (3 prompts)" "Secciones del README de Cristian." "parte-cristian,docs" "$CRISTIAN"

crear "P1: base.html y UI global" "Navbar responsivo, messages, footer, 403/404, estilos cv-." parte-pablo "$PABLO"
crear "P2: Registro y perfil" "RegistroForm con RUT (módulo 11) y teléfono; crea User y Perfil." parte-pablo "$PABLO"
crear "P3: Login y logout seguros" "Logout por POST, redirecciones correctas." parte-pablo "$PABLO"
crear "P4: Permisos por rol" "@login_required y @user_passes_test(es_staff); 403 con mensaje." parte-pablo "$PABLO"
crear "P5: R - Catálogo público" "Cards, Q multi-campo, filtro por género, orden con lista blanca, Paginator." parte-pablo "$PABLO"
crear "P6: R - Detalle por slug" "Datos, imagen y formulario POST hacia reservas:agregar." parte-pablo "$PABLO"
crear "P7: C - Crear espectáculo" "ModelForm Bootstrap, request.FILES, clean_ (código único, precio no negativo, cupos <= aforo)." parte-pablo "$PABLO"
crear "P8: U - Editar espectáculo" "Formulario precargado, unicidad excluyendo el propio registro." parte-pablo "$PABLO"
crear "P9: D - Eliminar (confirmación y baja lógica)" "Manejar ProtectedError en géneros." parte-pablo "$PABLO"
crear "P10: Listado de gestión (staff)" "Todos los registros, activos e inactivos." parte-pablo "$PABLO"
crear "P11: Pruebas de vistas y permisos" "Anónimo, cliente y staff." parte-pablo "$PABLO"
crear "P12: Documentación y bitácora IA (3 prompts)" "Secciones del README de Pablo." "parte-pablo,docs" "$PABLO"
echo "Issues creados."
