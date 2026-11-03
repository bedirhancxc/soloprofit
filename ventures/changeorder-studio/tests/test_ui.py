from pathlib import Path
from playwright.sync_api import sync_playwright

HTML=Path(__file__).resolve().parents[1].joinpath('index.html').read_text()
SHIM="""() => { const mem = {}; Object.defineProperty(window, 'localStorage', {configurable: true, value: {getItem:k=>mem[k]??null,setItem:(k,v)=>{mem[k]=String(v)},removeItem:k=>{delete mem[k]}}}); }"""
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width,height in [(1440,900),(390,844)]:
        context=browser.new_context(viewport={'width':width,'height':height},accept_downloads=True)
        page=context.new_page()
        errs=[]
        page.on('pageerror',lambda e:errs.append(str(e)))
        page.goto('about:blank')
        page.evaluate(SHIM)
        page.set_content(HTML,wait_until='load')
        assert page.title()=='Free Change Order Generator for Freelancers | ChangeOrder Studio'
        assert page.locator('#p-fee').inner_text()=='$375.00'
        page.locator('#project').fill('Brand refresh')
        page.locator('#client').fill('Acme Media')
        page.locator('#description').fill('Design 2 additional pages')
        page.locator('#hours').fill('6')
        page.locator('#rate').fill('90')
        assert page.locator('#p-fee').inner_text()=='$540.00'
        page.get_by_role('button',name='Save to my tracker').click()
        assert page.locator('#stat-count').inner_text()=='1'
        assert page.locator('.record h3').count()==1
        page.locator('.record select').select_option('Sent')
        assert page.locator('#stat-pending').inner_text()=='$540.00'
        page.locator('.record select').select_option('Approved')
        assert page.locator('#stat-approved').inner_text()=='$540.00'
        saved=page.evaluate('localStorage.getItem("changeorder-studio-v1")')
        assert 'Brand refresh' in saved and 'Approved' in saved
        page.get_by_role('button',name='Open').click()
        assert page.locator('#project').input_value()=='Brand refresh'
        assert page.locator('#p-fee').inner_text()=='$540.00'
        page.locator('#flatFee').fill('225')
        assert page.locator('#p-fee').inner_text()=='$225.00'
        page.locator('#currency').select_option('EUR')
        assert '225.00' in page.locator('#p-fee').inner_text()
        with page.expect_download() as info:
            page.locator('#export').click()
        assert info.value.suggested_filename.startswith('changeorder-backup')
        page.screenshot(path=f'/mnt/data/changeorder-{width}.png',full_page=True)
        if width==390:
            assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth'), 'mobile horizontal overflow'
        assert not errs, errs
        print(f'PASS {width}px: live calc, local save, statuses, fee override, currencies, backup download, no JS errors; localStorage simulated')
        context.close()
    browser.close()