from app.models import Customer, Staff, InventoryItem, Transaction

def test_get_customers(client, init_db):
    """Test to retrieve all customers."""
    # Add a test customer to the database
    customer = Customer(c_name="John Doe", c_email="john@example.com", c_contact="1234567890")
    init_db.session.add(customer)
    init_db.session.commit()

    # Test the GET /customers/ endpoint
    response = client.get('/customers/')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]['name'] == "John Doe"

def test_get_customer_by_id(client, init_db):
    """Test to retrieve a specific customer by ID."""
    # Add a test customer
    customer = Customer(c_name="Jane Doe", c_email="jane@example.com", c_contact="0987654321")
    init_db.session.add(customer)
    init_db.session.commit()

    # Test the GET /customers/<id>/ endpoint
    response = client.get(f'/customers/{customer.c_id}/')
    assert response.status_code == 200
    data = response.json
    assert data['name'] == "Jane Doe"
    assert data['email'] == "jane@example.com"
    assert data['contact'] == 987654321

def test_add_customer(client, init_db):
    """Test to add a new customer."""
    new_customer = {
        "name": "Alice",
        "email": "alice@example.com",
        "contact": "1122334455"
    }
    response = client.post('/customers/', json=new_customer)
    assert response.status_code == 201
    assert response.json['message'] == "Customer added successfully"

    # Verify the customer was added to the database
    customer = Customer.query.filter_by(c_email="alice@example.com").first()
    assert customer is not None
    assert customer.c_name == "Alice"

def test_update_customer(client, init_db):
    """Test to update an existing customer."""
    # Add a test customer
    customer = Customer(c_name="Bob", c_email="bob@example.com", c_contact="4455667788")
    init_db.session.add(customer)
    init_db.session.commit()

    # Update the customer's details
    updated_customer = {
        "name": "Bob Updated",
        "email": "bob.updated@example.com",
        "contact": "9988776655"
    }
    response = client.put(f'/customers/{customer.c_id}/', json=updated_customer)
    assert response.status_code == 200
    assert response.json['message'] == "Customer updated successfully"

    # Verify the update in the database
    updated_customer_in_db = Customer.query.get(customer.c_id)
    assert updated_customer_in_db.c_name == "Bob Updated"
    assert updated_customer_in_db.c_email == "bob.updated@example.com"

def test_delete_customer(client, init_db):
    """Test to delete a customer."""
    # Add a test customer
    customer = Customer(c_name="Charlie", c_email="charlie@example.com", c_contact="1122445566")
    init_db.session.add(customer)
    init_db.session.commit()

    # Delete the customer
    response = client.delete(f'/customers/{customer.c_id}/')
    assert response.status_code == 200
    assert response.json['message'] == "Customer deleted successfully"

    # Verify the customer is deleted from the database
    deleted_customer = Customer.query.get(customer.c_id)
    assert deleted_customer is None

def test_get_staff(client, init_db):
    """Test to retrieve all staff members."""
    response = client.get('/staff/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_inventory(client, init_db):
    """Test to retrieve all inventory items."""
    response = client.get('/inventory/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_transactions(client, init_db):
    """Test to retrieve all transactions."""
    response = client.get('/transactions/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_add_transaction(client, init_db):
    """Test to add a new transaction."""
    # Add a test customer and staff member
    customer = Customer(c_name="Test Customer", c_email="test.customer@example.com", c_contact="1231231234")
    staff = Staff(s_name="Test Staff", s_email="test.staff@example.com", s_is_admin=False, s_contact="4564564567")
    init_db.session.add(customer)
    init_db.session.add(staff)
    init_db.session.commit()

    # Add a new transaction
    new_transaction = {
        "customer_id": customer.c_id,
        "staff_id": staff.s_id,
        "date": "2024-12-18",
        "amount": 200.0,
        "category": "Purchase"
    }
    response = client.post('/transactions/', json=new_transaction)
    assert response.status_code == 201
    assert response.json['message'] == "Transaction added successfully"

