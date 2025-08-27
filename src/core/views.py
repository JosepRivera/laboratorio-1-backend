# src/core/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Item

# GET /api/items/ - Obtener todos los items
# POST /api/items/ - Crear nuevo item
@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_items(request):
    if request.method == "GET":
        items = Item.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "created_at": item.created_at.isoformat(),
                }
            )
        return JsonResponse({"success": True, "items": data, "count": len(data)})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            # Validar datos requeridos
            if not data.get("name"):
                return JsonResponse(
                    {"success": False, "error": "Name is required"}, status=400
                )

            # Crear nuevo item
            item = Item.objects.create(
                name=data["name"], description=data.get("description", "")
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": "Item created successfully",
                    "item": {
                        "id": item.id,
                        "name": item.name,
                        "description": item.description,
                        "created_at": item.created_at.isoformat(),
                    },
                },
                status=201,
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


# GET /api/items/<id>/ - Obtener item específico
# PUT /api/items/<id>/ - Actualizar item
# DELETE /api/items/<id>/ - Eliminar item
@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_item_detail(request, item_id):
    try:
        item = get_object_or_404(Item, id=item_id)
    except:
        return JsonResponse({"success": False, "error": "Item not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(
            {
                "success": True,
                "item": {
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "created_at": item.created_at.isoformat(),
                },
            }
        )

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)

            # Actualizar campos si están presentes
            if "name" in data:
                item.name = data["name"]
            if "description" in data:
                item.description = data["description"]

            item.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Item updated successfully",
                    "item": {
                        "id": item.id,
                        "name": item.name,
                        "description": item.description,
                        "created_at": item.created_at.isoformat(),
                    },
                }
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    elif request.method == "DELETE":
        try:
            item_name = item.name
            item.delete()
            return JsonResponse(
                {"success": True, "message": f'Item "{item_name}" deleted successfully'}
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
