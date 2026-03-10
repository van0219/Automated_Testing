# FSM Navigation Discovery - NMR2N66J9P445R7P_AX4 Tenant

## Date: March 5, 2026
## Discovered using: Playwright MCP Tools

---

## KEY FINDING: FSM Content is in an IFRAME!

The FSM application content is embedded in an iframe, NOT in the main page DOM. This is why standard selectors weren't working.

**Iframe selector**: `iframe[name="fsm_41_03b3ab89-37e0-4632-a578-7700d803b32e"]`

---

## Login Flow

### Step 1: Navigate to Portal
- **URL**: `https://mingle-portal.inforcloudsuite.com/v2/NMR2N66J9P445R7P_AX4`
- **Redirects to**: Authentication selection page
- **Page Title**: "Choose Authentication"
- **Wait time**: 3 seconds

### Step 2: Select Authentication Method
- **Element**: Link "Cloud Identities"
- **Selector**: `page.getByRole('link', { name: 'Cloud Identities' })`
- **Action**: Click
- **Result**: Redirects to login page
- **Wait time**: 5 seconds

### Step 3: Enter Credentials
- **Username field**: `page.getByRole('textbox', { name: 'Username' })`
- **Password field**: `page.getByRole('textbox', { name: 'Password' })`
- **Sign in button**: `page.getByRole('button', { name: 'Sign in' })`
- **Wait time after login**: 8-10 seconds

### Step 4: Portal Loads
- **Page Title**: "Infor OS Portal" → "Financials & Supply Management"
- **Final URL**: Contains `/v2/NMR2N66J9P445R7P_AX4/03b3ab89-37e0-4632-a578-7700d803b32e`

---

## Navigate to Payables

### CRITICAL: Work with Iframe Content

All FSM application elements are inside an iframe. You MUST:
1. Get the iframe: `page.locator('iframe[name^="fsm_"]').contentFrame()`
2. Then interact with elements inside the iframe

### IMPORTANT: Two Navigation Scenarios

The navigation depends on whether Payables is set as the user's preferred application:

#### Scenario A: Payables NOT Preferred (First Time)
User sees "My Available Applications" page and must navigate to Payables

#### Scenario B: Payables IS Preferred
Payables loads automatically after login

**Framework must detect which scenario and handle accordingly!**

---

### Scenario A: Navigate from "My Available Applications"

#### Step 1: FSM Page Loads
- **Page Title**: "Financials & Supply Management"
- **Content**: "My Available Applications" page (inside iframe)
- **Detection**: Look for heading "My Available Applications" inside iframe
- **Wait time**: 8 seconds after login

#### Step 2: Click Payables Application
- **Element**: Button "More - Payables" (inside iframe)
- **Selector**: `iframe.contentFrame().getByRole('button', { name: 'More - Payables' })`
- **Action**: Click
- **Result**: Confirmation dialog appears

#### Step 3: Confirm Preferred Application (OPTIONAL)
- **Dialog**: "Confirmation Required" - asks if you want Payables as preferred start app
- **Element**: Button "Ok" (inside iframe)
- **Selector**: `iframe.contentFrame().getByRole('button', { name: 'Ok' })`
- **Action**: Click if dialog appears
- **Note**: Dialog only appears FIRST TIME user accesses Payables
- **Result**: Payables application loads

#### Step 4: Payables Loads
- **Page Title**: Still "Financials & Supply Management"
- **URL Changes**: Contains `/Payables/page/PayablesSearchUX1`
- **Content**: "Search Invoices" page with search fields and "Create Invoice" button
- **Wait time**: 10 seconds

---

### Scenario B: Payables Already Preferred

#### Step 1: FSM Page Loads with Payables
- **Page Title**: "Financials & Supply Management"
- **URL**: Already contains `/Payables/page/PayablesSearchUX1`
- **Content**: "Search Invoices" page loads directly (inside iframe)
- **Detection**: Look for "Create Invoice" button inside iframe
- **Wait time**: 8-10 seconds after login
- **Action**: No navigation needed, already on Payables!

---

### Detection Logic (Recommended)

```python
# Wait for iframe to load
iframe = page.frame_locator('iframe[name^="fsm_"]')
page.wait_for_timeout(8000)

# Check if already on Payables (Scenario B)
try:
    if iframe.get_by_role('button', name='Create Invoice').is_visible(timeout=3000):
        # Already on Payables, no navigation needed
        return
except:
    pass

# Check if on "My Available Applications" (Scenario A)
try:
    if iframe.get_by_role('heading', name='My Available Applications').is_visible(timeout=3000):
        # Need to navigate to Payables
        iframe.get_by_role('button', name='More - Payables').click()
        
        # Handle confirmation dialog if it appears
        try:
            iframe.get_by_role('button', name='Ok').click(timeout=5000)
        except:
            pass  # Dialog didn't appear
        
        # Wait for Payables to load
        page.wait_for_timeout(10000)
except:
    raise Exception("Unknown FSM page state")
```

---

## Payables Page Elements

### Navigation Tabs (inside iframe)
- Invoices
- My Invoices
- Payments
- Vendors
- Tax and Income
- Period End Close
- Interfaces
- Administration

### Key Buttons (inside iframe)
- **Create Invoice**: `iframe.contentFrame().getByRole('button', { name: 'Create Invoice' })`
- **Create and Release**: `iframe.contentFrame().getByRole('button', { name: 'Create and Release' })`
- **Search**: `iframe.contentFrame().getByRole('button', { name: 'Search' })`
- **Advanced Search**: `iframe.contentFrame().getByRole('button', { name: 'Advanced Search' })`

### Search Fields (inside iframe)
- Keyword
- Company (with lookup)
- Vendor (with lookup)
- Invoice Number
- Status (dropdown)
- Invoice Date (date picker)
- Due Date (date picker)
- Invoice Amount
- SONH Comment Text

---

## Total Wait Times

| Step | Wait Time | Notes |
|------|-----------|-------|
| After navigate to portal | 3 seconds | Authentication page loads |
| After click Cloud Identities | 5 seconds | Login page loads |
| After sign in | 8-10 seconds | Portal and FSM load |
| After click Payables | 10 seconds | Payables application loads |
| **Total from start to Payables** | **26-28 seconds** | Full navigation time |

---

## Code Implementation Notes

### Python Playwright (Standard)

```python
# Get iframe
iframe = page.frame_locator('iframe[name^="fsm_"]')

# Click Payables
iframe.get_by_role('button', name='More - Payables').click()

# Confirm dialog
iframe.get_by_role('button', name='Ok').click()

# Wait for Payables to load
page.wait_for_timeout(10000)

# Click Create Invoice
iframe.get_by_role('button', name='Create Invoice').click()
```

### Key Differences from Expected

1. **Iframe**: FSM content is in iframe, not main page
2. **Application Selection**: Must click "More - Payables" button, not a link
3. **Confirmation Dialog**: Appears first time accessing Payables
4. **Wait Times**: Longer than expected (10 seconds for Payables to load)

---

## Recommendations for Framework

1. **Add iframe support**: All FSM actions must work with iframe content
2. **Update selectors**: Use role-based selectors (more reliable)
3. **Increase wait times**: Current 3-5 second waits are too short
4. **Handle TWO navigation scenarios**: 
   - Scenario A: Navigate from "My Available Applications" (first time)
   - Scenario B: Payables already preferred (subsequent times)
5. **Handle optional confirmation dialog**: Only appears first time
6. **Use adaptive waits**: Wait for specific elements, not fixed timeouts
7. **Detect page state**: Check which scenario before attempting navigation

---

## Next Steps

1. Update `fsm_payables.py` to work with iframe
2. Update `fsm_login.py` to use correct selectors
3. Test invoice creation flow inside iframe
4. Document Work Units navigation (also in iframe)
