"""Template Pets endpoints."""

__all__ = (
    'delete',
    'insert',
    'read',
    'replace',
    'update',
    )

from ... api import Request

from .. import pkg


@pkg.obj.Pet.DELETE
def delete(request: Request) -> None:
    """Delete a single record."""

    if isinstance(request.body, dict):
        parent_id = request.path_params['petWithPetId']
        id_ = request.path_params['petId']
        pet_with_pet: pkg.obj.PetWithPet = (
            pkg.clients.DatabaseClient.find_one(parent_id)
            )
        if pet_with_pet is None:
            raise FileNotFoundError
        pet_with_pet.pets = [
            pet
            for pet
            in pet_with_pet.pets
            if pet.id_ != id_
            ]
        pkg.clients.DatabaseClient.update_one(pet_with_pet)
    else:
        raise SyntaxError

    return None


@pkg.obj.Pet.GET
def read(request: Request) -> pkg.obj.Pet:
    """Read a single record."""

    parent_id = request.path_params['petWithPetId']
    id_ = request.path_params['petId']

    pet_with_pet: pkg.obj.PetWithPet = (
        pkg.clients.DatabaseClient.find_one(parent_id)
        )

    if pet_with_pet is None:
        raise FileNotFoundError

    for pet in pet_with_pet.pets:
        if pet.id_ == id_:
            return pet

    raise FileNotFoundError


@pkg.obj.Pet.PATCH
def update(request: Request) -> pkg.obj.Pet:
    """Update a single record."""

    if isinstance(request.body, dict):
        parent_id = request.path_params['petWithPetId']
        id_ = request.path_params['petId']

        pet_with_pet: pkg.obj.PetWithPet = (
            pkg.clients.DatabaseClient.find_one(parent_id)
            )

        if pet_with_pet is None:
            raise FileNotFoundError

        for pet in pet_with_pet.pets:
            if pet.id_ == id_:
                pet.update(request.query_params)
                pkg.clients.DatabaseClient.update_one(pet_with_pet)
                return pet

        raise FileNotFoundError
    else:
        raise SyntaxError


@pkg.obj.Pet.POST
def insert(request: Request) -> pkg.obj.Pet:
    """Insert single record."""

    if isinstance(request.body, dict):
        parent_id = request.path_params['petWithPetId']

        pet_with_pet: pkg.obj.PetWithPet = (
            pkg.clients.DatabaseClient.find_one(parent_id)
            )

        if pet_with_pet is None:
            raise FileNotFoundError

        pet = pkg.obj.Pet(pet_with_pet_id=parent_id, **request.body)  # type: ignore[misc]
        pet_with_pet.pets.append(pet)
        pkg.clients.DatabaseClient.update_one(pet_with_pet)

        return pet
    else:
        raise SyntaxError


@pkg.obj.Pet.PUT
def replace(request: Request) -> pkg.obj.Pet:
    """Replace a single record."""

    if isinstance(request.body, dict):
        parent_id = request.path_params['petWithPetId']
        id_ = request.path_params['petId']

        pet_with_pet: pkg.obj.PetWithPet = (
            pkg.clients.DatabaseClient.find_one(parent_id)
            )

        if pet_with_pet is None:
            raise FileNotFoundError

        for pet in pet_with_pet.pets:
            if pet.id_ == id_:
                pet.update(request.body)  # type: ignore[arg-type]
                pkg.clients.DatabaseClient.update_one(pet_with_pet)
                return pet

        raise FileNotFoundError
    else:
        raise SyntaxError
