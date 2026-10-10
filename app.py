import random
import streamlit as st

st.set_page_config(page_title="El Reino de los Números Mágicos", page_icon="🦄", layout="centered")

st.markdown(
    """
<style>
.stApp { background: linear-gradient(160deg, #fff0f8 0%, #f1e8ff 50%, #e6f4ff 100%); }
h1, h2, h3 { color: #8e3fb5 !important; }
.stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp small,
.stApp [data-testid="stMarkdownContainer"], .stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stWidgetLabel"] p, .stApp [data-testid="stMetricLabel"] p,
.stApp [data-testid="stMetricValue"], .stApp button[data-baseweb="tab"] p,
.stApp [data-baseweb="radio"] div { color: #3b2a55 !important; }
.stApp h1, .stApp h2, .stApp h3 { color: #8e3fb5 !important; }
.stApp .big { color: #8e3fb5 !important; }
.stApp button[data-baseweb="tab"][aria-selected="true"] p { color: #c2185b !important; font-weight: 800; }
[data-testid="stSidebar"] { background: #f6ebff; }
.stApp input { color: #3b2a55 !important; background: #ffffff !important; }
.card { background: #ffffffcc; border: 2px dashed #d9a7f0; border-radius: 18px;
        padding: 14px 18px; margin: 10px 0; font-size: 1.15rem; }
.big { font-size: 2.2rem; text-align: center; color: #8e3fb5; font-weight: 800; }
.rule { background: #e8f3ff; border-left: 6px solid #6cb4ee; border-radius: 12px;
        padding: 10px 14px; margin: 8px 0; }
.stButton button, .stFormSubmitButton button { border-radius: 20px; font-weight: 700; }
</style>
""",
    unsafe_allow_html=True,
)

ss = st.session_state
for k, v in {"qid": 0, "results": {}, "score": 0, "total": 0, "streak": 0, "just": None}.items():
    if k not in ss:
        ss[k] = v

# ---------------------------------------------------------------- utilidades
UN = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
      "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete",
      "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós", "veintitrés",
      "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
DEC = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
CEN = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos",
       6: "seiscientos", 7: "setecientos", 8: "ochocientos", 9: "novecientos"}
POS = ["U", "D", "C", "UM"]
NOMBRE = {"U": "unidades", "D": "decenas", "C": "centenas", "UM": "unidades de millar"}
VALOR = {"U": 1, "D": 10, "C": 100, "UM": 1000}


def bajo100(n):
    if n < 30:
        return UN[n]
    d, u = divmod(n, 10)
    return DEC[d] if u == 0 else f"{DEC[d]} y {UN[u]}"


def bajo1000(n):
    if n == 100:
        return "cien"
    c, r = divmod(n, 100)
    partes = []
    if c:
        partes.append(CEN[c])
    if r:
        partes.append(bajo100(r))
    return " ".join(partes)


def palabras(n):
    m, r = divmod(n, 1000)
    txt = []
    if m:
        txt.append("mil" if m == 1 else f"{UN[m]} mil")
    if r:
        txt.append(bajo1000(r))
    return " ".join(txt)


def digitos(n):
    s = f"{n:04d}"
    return [int(x) for x in s]  # UM, C, D, U


def fmt(n):
    return f"{n:,}".replace(",", ".") if n >= 10000 else str(n)


def descomposicion(n):
    um, c, d, u = digitos(n)
    return (f"{um} UM + {c} C + {d} D + {u} U",
            f"{um} × 1000 + {c} × 100 + {d} × 10 + {u} × 1",
            f"{um*1000} + {c*100} + {d*10} + {u}")


def aprox(n, a):
    base = 100 if a == "centenas" else 1000
    bajo = n // base * base
    alto = bajo + base
    return bajo, alto, (bajo if n - bajo < alto - n else alto)


def comparar_texto(a, b):
    if a == b:
        return f"{a} = {b}: son iguales."
    la, lb = len(str(a)), len(str(b))
    if la != lb:
        mayor, menor = (a, b) if la > lb else (b, a)
        return (f"{a} tiene {la} cifras y {b} tiene {lb}. Tiene más cifras el {mayor}, "
                f"así que {mayor} > {menor}.")
    sa, sb = str(a), str(b)
    nombres = ["UM", "C", "D", "U"][-la:]
    for i in range(la):
        if sa[i] != sb[i]:
            mayor, menor = (a, b) if sa[i] > sb[i] else (b, a)
            return (f"Tienen {la} cifras. Comparo de izquierda a derecha: en las {NOMBRE[nombres[i]]} "
                    f"({nombres[i]}) {sa[i]} y {sb[i]} son distintas. "
                    f"{max(sa[i], sb[i])} > {min(sa[i], sb[i])}, así que {mayor} > {menor}.")
    return ""


# ---------------------------------------------------------------- preguntas
def q_descomponer():
    n = random.randint(1000, 9999)
    um, c, d, u = digitos(n)
    return dict(kind="number", answer=n,
                prompt=f"🧚 ¿Qué número es **{um} UM + {c} C + {d} D + {u} U**?",
                expl=f"{descomposicion(n)[2]} = {n}")


def q_valor():
    while True:
        n = random.randint(1000, 9999)
        i = random.randint(0, 3)
        dig = digitos(n)[i]
        if dig:
            break
    pos = ["UM", "C", "D", "U"][i]
    return dict(kind="number", answer=dig * VALOR[pos],
                prompt=f"🦄 En el número **{n}**, ¿cuál es el valor de la cifra **{dig}** (en unidades)?"
                       if digitos(n).count(dig) == 1 else
                       f"🦄 En el número **{n}**, ¿cuál es el valor de la cifra de las **{NOMBRE[pos]}** ({pos}), en unidades?",
                expl=f"La cifra {dig} ocupa el lugar de las {NOMBRE[pos]}, así que vale {dig} × {VALOR[pos]} = {dig*VALOR[pos]}.")


def q_escribir():
    n = random.randint(1000, 9999)
    return dict(kind="number", answer=n,
                prompt=f"✍️ Escribe con cifras: **{palabras(n).capitalize()}**.",
                expl=f"{palabras(n).capitalize()} se escribe {n}.")


def q_leer():
    n = random.randint(1000, 9999)
    opciones = {n}
    while len(opciones) < 3:
        s = list(str(n))
        i = random.randint(0, 3)
        s[i] = str((int(s[i]) + random.randint(1, 8)) % 10 or 1)
        m = int("".join(s))
        if m >= 1000:
            opciones.add(m)
    ops = [palabras(x).capitalize() for x in opciones]
    random.shuffle(ops)
    return dict(kind="choice", answer=palabras(n).capitalize(), options=ops,
                prompt=f"📖 ¿Cómo se lee el número **{n}**?",
                expl=f"{n} se lee: {palabras(n)}.")


def q_equiv():
    a, b, f = random.choice([("UM", "C", 10), ("UM", "D", 100), ("UM", "U", 1000),
                             ("C", "D", 10), ("C", "U", 100), ("D", "U", 10)])
    k = random.randint(2, 9)
    return dict(kind="number", answer=k * f,
                prompt=f"🔢 Completa: **{k} {a} = ? {b}**",
                expl=f"1 {a} = {f} {b}, así que {k} {a} = {k} × {f} = {k*f} {b}.")


def q_recta():
    s = random.randint(1000, 9997)
    if random.random() < .5:
        return dict(kind="number", answer=s + 1,
                    prompt=f"📏 En la recta numérica, ¿qué número está entre **{s}** y **{s+2}**?",
                    expl=f"Entre {s} y {s+2} está {s+1}.")
    n = random.choice([999, 1999, 2999, 3999, 4999, 5999, 6999, 7999, 8999])
    return dict(kind="number", answer=n + 1,
                prompt=f"📏 ¿Qué número viene justo después de **{n}**?",
                expl=f"Después de {n} viene {n+1}" + (" y se llama *mil*." if n == 999 else "."))


def q_comparar():
    r = random.random()
    if r < .25:
        a, b = random.randint(100, 999), random.randint(1000, 9999)
    elif r < .85:
        a = random.randint(1000, 9999)
        b = a + random.choice([-1, 1]) * random.choice([1, 8, 20, 90, 200, 400, 1000])
        b = min(max(b, 1000), 9999)
    else:
        a = random.randint(1000, 9999)
        b = a
    if random.random() < .5:
        a, b = b, a
    res = "=" if a == b else (">" if a > b else "<")
    return dict(kind="choice", answer=res, options=["<", "=", ">"],
                prompt=f"⚖️ Compara: **{a}  ?  {b}**",
                expl=comparar_texto(a, b))


def q_aprox_c():
    n = random.randint(1001, 9949)
    while n % 100 == 0:
        n = random.randint(1001, 9949)
    b, a, r = aprox(n, "centenas")
    return dict(kind="number", answer=r,
                prompt=f"🎯 Aproxima **{n}** a las **centenas**.",
                expl=f"{n} está entre {b} y {a}. {n} − {b} = {n-b} y {a} − {n} = {a-n}. "
                     f"La menor diferencia es con {r}, así que se aproxima a {r}.")


def q_aprox_um():
    n = random.randint(1001, 9499)
    while n % 1000 == 0:
        n = random.randint(1001, 9499)
    b, a, r = aprox(n, "unidades de millar")
    c = digitos(n)[1]
    return dict(kind="number", answer=r,
                prompt=f"🎯 Aproxima **{n}** a las **unidades de millar**.",
                expl=f"La cifra de las centenas es {c}. " +
                     (f"{c} es menor que 5, la unidad de millar se queda igual: {r}." if c < 5
                      else f"{c} es igual o mayor que 5, se suma 1 a las unidades de millar: {r}."))


TEMAS = {
    "🔢 Números de cuatro cifras": [q_descomponer, q_valor, q_escribir, q_leer, q_equiv, q_recta],
    "⚖️ Comparar números": [q_comparar],
    "🎯 Aproximar números": [q_aprox_c, q_aprox_um],
}
TEMAS["🌈 Mezcla mágica"] = [g for gens in list(TEMAS.values()) for g in gens]

FELICITA = ["¡Brillante como un unicornio! 🦄", "¡Magia pura! ✨", "¡Las hadas aplauden! 🧚",
            "¡Perfecto! 🌈", "¡Eres una crack de los números! 💖"]
ANIMO = ["¡Casi! Las hadas te ayudan a verlo 🧚", "No pasa nada, ¡a por la siguiente! 🦄",
         "Mira la explicación y lo tendrás ✨"]


def nueva(gens):
    ss.qid += 1
    q = random.choice(gens)()
    q["id"] = ss.qid
    return q


def practicar(tema, gens):
    k = f"cur_{tema}"
    if k not in ss:
        ss[k] = nueva(gens)
    q = ss[k]
    qid = q["id"]
    hecho = qid in ss.results
    st.markdown(f"<div class='card'>{q['prompt']}</div>", unsafe_allow_html=True)
    with st.form(f"form_{qid}"):
        if q["kind"] == "number":
            resp = st.number_input("Tu respuesta", min_value=0, max_value=99999, value=None, step=1,
                                   format="%d", placeholder="Escribe aquí el número", key=f"a_{qid}",
                                   disabled=hecho)
        else:
            resp = st.radio("Elige una opción", q["options"], index=None, key=f"a_{qid}",
                            disabled=hecho, horizontal=True)
        enviado = st.form_submit_button("✨ Comprobar", disabled=hecho)
    if enviado and not hecho:
        if resp is None:
            st.warning("Escribe o elige una respuesta primero 😊")
        else:
            ok = resp == q["answer"]
            ss.results[qid] = ok
            ss.total += 1
            ss.score += int(ok)
            ss.streak = ss.streak + 1 if ok else 0
            ss.just = qid
            st.rerun()
    if qid in ss.results:
        if ss.results[qid]:
            st.success(random.choice(FELICITA))
            if ss.just == qid and ss.streak and ss.streak % 5 == 0:
                st.balloons()
        else:
            st.error(random.choice(ANIMO))
        ss.just = None
        st.info(q["expl"])
        if st.button("Siguiente ➡️", key=f"next_{qid}"):
            ss[k] = nueva(gens)
            st.rerun()


# ---------------------------------------------------------------- barra lateral
with st.sidebar:
    st.header("🏆 Mis estrellas")
    st.metric("Aciertos", f"{ss.score} / {ss.total}")
    st.metric("Racha 🔥", ss.streak)
    estrellas = ss.score // 5
    st.markdown("### " + ("⭐" * estrellas if estrellas else "¡Consigue tu primera estrella con 5 aciertos!"))
    if estrellas:
        st.markdown("🦄" * min(estrellas, 10) + " " + "🧚" * min(estrellas // 2, 10))
    if st.button("Empezar de nuevo"):
        for key in list(ss.keys()):
            del ss[key]
        st.rerun()

# ---------------------------------------------------------------- cabecera
st.title("🦄 El Reino de los Números Mágicos 🧚")
st.caption("Matemáticas · Unidad 1 · 3.º de Primaria")

tab_aprender, tab_practicar = st.tabs(["📖 Aprender", "🎯 Practicar"])

# ---------------------------------------------------------------- APRENDER
with tab_aprender:
    t1, t2, t3 = st.tabs(["🔢 Cuatro cifras", "⚖️ Comparar", "🎯 Aproximar"])

    with t1:
        st.header("Conocer los números de cuatro cifras")
        st.markdown(
            "<div class='rule'>El número siguiente a 999 se llama <b>mil</b> y se escribe 1000.<br>"
            "Los números de cuatro cifras tienen <b>unidades de millar (UM), centenas (C), "
            "decenas (D) y unidades (U)</b>.</div>", unsafe_allow_html=True)
        st.markdown("**1 UM = 10 C = 100 D = 1 000 U**")
        st.subheader("🪄 Construye tu número")
        cols = st.columns(4)
        um = cols[0].slider("UM", 1, 9, 5)
        c = cols[1].slider("C", 0, 9, 3)
        d = cols[2].slider("D", 0, 9, 4)
        u = cols[3].slider("U", 0, 9, 2)
        n = um * 1000 + c * 100 + d * 10 + u
        st.markdown(f"<div class='big'>{n}</div>", unsafe_allow_html=True)
        d1, d2, d3 = descomposicion(n)
        st.markdown(f"- {n} = {d1}\n- {n} = {d2}\n- {n} = {d3}")
        st.markdown(f"**Se lee:** {palabras(n)} 🧚")
        st.markdown("<div class='rule'>El <b>valor de cada cifra</b> depende de la <b>posición</b> que ocupa. "
                    f"Por ejemplo, en {n}: la cifra {u} vale {u} unidades, la cifra {d} vale {d*10}, "
                    f"la cifra {c} vale {c*100} y la cifra {um} vale {um*1000}.</div>", unsafe_allow_html=True)
        st.subheader("📖 Lectura")
        st.markdown("Se empieza por las unidades de millar, luego la palabra **mil**, y después "
                    "se lee el número formado por las tres cifras siguientes.\n\n"
                    "Ejemplo: 5 | 342 → **cinco mil** trescientos cuarenta y dos.")
        st.subheader("📏 Recta numérica")
        st.code("996  997  998  999  1000  1001  1002  1003  1004  1005  1006")
        st.caption("Después del 999 viene el 1000 ✨")

    with t2:
        st.header("Comparar números")
        st.markdown(
            "<div class='rule'>• Si tienen <b>distinta cantidad de cifras</b>, es menor el que tiene menos "
            "cifras.<br>• Si tienen la <b>misma cantidad de cifras</b>, se comparan cifra a cifra, "
            "empezando por la izquierda.<br>• En la recta numérica, el que está a la derecha es mayor.</div>",
            unsafe_allow_html=True)
        st.markdown("`=` igual que · `>` mayor que · `<` menor que")
        st.subheader("🪄 Prueba con tus números")
        c1, c2 = st.columns(2)
        a = c1.number_input("Primer número", 0, 9999, 1346, step=1)
        b = c2.number_input("Segundo número", 0, 9999, 1328, step=1)
        sig = "=" if a == b else (">" if a > b else "<")
        st.markdown(f"<div class='big'>{a} {sig} {b}</div>", unsafe_allow_html=True)
        st.write(comparar_texto(int(a), int(b)))

    with t3:
        st.header("Aproximar números")
        st.markdown("<div class='rule'>Para <b>aproximar</b> un número hay que encontrar la decena, la "
                    "centena o la unidad de millar <b>más cercana</b>. Se mira entre qué números está, "
                    "se comparan las diferencias y se elige la más cercana.</div>", unsafe_allow_html=True)
        st.subheader("🪄 Prueba con tu número")
        n = int(st.number_input("Número", 1, 9999, 440, step=1, key="aprox_n"))
        modo = st.radio("Aproximar a las…", ["centenas", "unidades de millar"], horizontal=True)
        b, a, r = aprox(n, modo)
        st.markdown(f"**{n}** está entre **{b}** y **{a}**.")
        st.progress((n - b) / (a - b))
        st.caption(f"{b}  ←  {n}  →  {a}")
        st.markdown(f"- {a} − {n} = {a-n}\n- {n} − {b} = {n-b}")
        st.markdown(f"<div class='big'>{n} ≈ {r}</div>", unsafe_allow_html=True)
        st.subheader("✨ Otra forma de aproximar")
        st.markdown("Para aproximar a las **unidades de millar**, mira la cifra de las **centenas**:\n\n"
                    "- Si es **menor que 5**, la unidad de millar se queda igual. (6200 → 6000)\n"
                    "- Si es **igual o mayor que 5**, se suma 1 a la unidad de millar. (6800 → 7000)")

# ---------------------------------------------------------------- PRACTICAR
with tab_practicar:
    st.header("¡Ponte a prueba!")
    tema = st.radio("Elige un tema", list(TEMAS.keys()), horizontal=False)
    practicar(tema, TEMAS[tema])
