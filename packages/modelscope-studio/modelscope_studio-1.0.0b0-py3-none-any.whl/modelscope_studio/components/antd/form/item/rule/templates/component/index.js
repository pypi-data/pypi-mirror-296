function R(e) {
  const {
    gradio: t,
    _internal: s,
    ...i
  } = e;
  return Object.keys(s).reduce((_, m) => {
    const u = m.match(/bind_(.+)_event/);
    if (u) {
      const l = u[1], n = l.split("_"), o = (...d) => {
        const f = d.map((r) => d && typeof r == "object" && (r.nativeEvent || r instanceof Event) ? {
          type: r.type,
          detail: r.detail,
          timestamp: r.timeStamp,
          clientX: r.clientX,
          clientY: r.clientY,
          targetId: r.target.id,
          targetClassName: r.target.className,
          altKey: r.altKey,
          ctrlKey: r.ctrlKey,
          shiftKey: r.shiftKey,
          metaKey: r.metaKey
        } : r);
        return t.dispatch(l.replace(/[A-Z]/g, (r) => "_" + r.toLowerCase()), {
          payload: f,
          component: i
        });
      };
      if (n.length > 1) {
        let d = {
          ...i.props[n[0]] || {}
        };
        _[n[0]] = d;
        for (let r = 1; r < n.length - 1; r++) {
          const b = {
            ...i.props[n[r]] || {}
          };
          d[n[r]] = b, d = b;
        }
        const f = n[n.length - 1];
        return d[`on${f.slice(0, 1).toUpperCase()}${f.slice(1)}`] = o, _;
      }
      const a = n[0];
      _[`on${a.slice(0, 1).toUpperCase()}${a.slice(1)}`] = o;
    }
    return _;
  }, {});
}
function p() {
}
function E(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function j(e, ...t) {
  if (e == null) {
    for (const i of t)
      i(void 0);
    return p;
  }
  const s = e.subscribe(...t);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function h(e) {
  let t;
  return j(e, (s) => t = s)(), t;
}
const x = [];
function g(e, t = p) {
  let s;
  const i = /* @__PURE__ */ new Set();
  function _(l) {
    if (E(e, l) && (e = l, s)) {
      const n = !x.length;
      for (const o of i)
        o[1](), x.push(o, e);
      if (n) {
        for (let o = 0; o < x.length; o += 2)
          x[o][0](x[o + 1]);
        x.length = 0;
      }
    }
  }
  function m(l) {
    _(l(e));
  }
  function u(l, n = p) {
    const o = [l, n];
    return i.add(o), i.size === 1 && (s = t(_, m) || p), l(e), () => {
      i.delete(o), i.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: _,
    update: m,
    subscribe: u
  };
}
const {
  getContext: S,
  setContext: v
} = window.__gradio__svelte__internal, z = "$$ms-gr-antd-context-key";
function M(e) {
  var l;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = q(), s = V({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((n) => {
    s.slotKey.set(n);
  }), N();
  const i = S(z), _ = ((l = h(i)) == null ? void 0 : l.as_item) || e.as_item, m = i ? _ ? h(i)[_] : h(i) : {}, u = g({
    ...e,
    ...m
  });
  return i ? (i.subscribe((n) => {
    const {
      as_item: o
    } = h(u);
    o && (n = n[o]), u.update((a) => ({
      ...a,
      ...n
    }));
  }), [u, (n) => {
    const o = n.as_item ? h(i)[n.as_item] : h(i);
    return u.set({
      ...n,
      ...o
    });
  }]) : [u, (n) => {
    u.set(n);
  }];
}
const k = "$$ms-gr-antd-slot-key";
function N() {
  v(k, g(void 0));
}
function q() {
  return S(k);
}
const U = "$$ms-gr-antd-component-slot-context-key";
function V({
  slot: e,
  index: t,
  subIndex: s
}) {
  return v(U, {
    slotKey: g(e),
    slotIndex: g(t),
    subSlotIndex: g(s)
  });
}
function w(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
const {
  getContext: X,
  setContext: Y
} = window.__gradio__svelte__internal;
function A(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function s(_ = ["default"]) {
    const m = _.reduce((u, l) => (u[l] = g([]), u), {});
    return Y(t, {
      itemsMap: m,
      allowedSlots: _
    }), m;
  }
  function i() {
    const {
      itemsMap: _,
      allowedSlots: m
    } = X(t);
    return function(u, l, n) {
      _ && (u ? _[u].update((o) => {
        const a = [...o];
        return m.includes(u) ? a[l] = n : a[l] = void 0, a;
      }) : m.includes("default") && _.default.update((o) => {
        const a = [...o];
        return a[l] = n, a;
      }));
    };
  }
  return {
    getItems: s,
    getSetItemFn: i
  };
}
const {
  getItems: G,
  getSetItemFn: L
} = A("form-item-rule"), {
  SvelteComponent: O,
  component_subscribe: C,
  flush: y,
  init: Z,
  safe_not_equal: B
} = window.__gradio__svelte__internal;
function D(e, t, s) {
  let i, _, m, {
    gradio: u
  } = t, {
    props: l = {}
  } = t;
  const n = g(l);
  C(e, n, (c) => s(13, m = c));
  let {
    _internal: o = {}
  } = t, {
    as_item: a
  } = t, {
    visible: d = !0
  } = t, {
    elem_id: f = ""
  } = t, {
    elem_classes: r = []
  } = t, {
    elem_style: b = {}
  } = t;
  const K = q();
  C(e, K, (c) => s(12, _ = c));
  const [I, F] = M({
    gradio: u,
    props: m,
    _internal: o,
    visible: d,
    elem_id: f,
    elem_classes: r,
    elem_style: b,
    as_item: a
  });
  C(e, I, (c) => s(11, i = c));
  const P = L();
  return e.$$set = (c) => {
    "gradio" in c && s(3, u = c.gradio), "props" in c && s(4, l = c.props), "_internal" in c && s(5, o = c._internal), "as_item" in c && s(6, a = c.as_item), "visible" in c && s(7, d = c.visible), "elem_id" in c && s(8, f = c.elem_id), "elem_classes" in c && s(9, r = c.elem_classes), "elem_style" in c && s(10, b = c.elem_style);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    16 && n.update((c) => ({
      ...c,
      ...l
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    10216 && F({
      gradio: u,
      props: m,
      _internal: o,
      visible: d,
      elem_id: f,
      elem_classes: r,
      elem_style: b,
      as_item: a
    }), e.$$.dirty & /*$slotKey, $mergedProps*/
    6144 && P(_, i._internal.index || 0, {
      props: {
        ...i.props,
        ...R(i),
        transform: w(i.props.transform),
        validator: w(i.props.validator)
      },
      slots: {}
    });
  }, [n, K, I, u, l, o, a, d, f, r, b, i, _, m];
}
class H extends O {
  constructor(t) {
    super(), Z(this, t, D, null, B, {
      gradio: 3,
      props: 4,
      _internal: 5,
      as_item: 6,
      visible: 7,
      elem_id: 8,
      elem_classes: 9,
      elem_style: 10
    });
  }
  get gradio() {
    return this.$$.ctx[3];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), y();
  }
  get props() {
    return this.$$.ctx[4];
  }
  set props(t) {
    this.$$set({
      props: t
    }), y();
  }
  get _internal() {
    return this.$$.ctx[5];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), y();
  }
  get as_item() {
    return this.$$.ctx[6];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), y();
  }
  get visible() {
    return this.$$.ctx[7];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), y();
  }
  get elem_id() {
    return this.$$.ctx[8];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), y();
  }
  get elem_classes() {
    return this.$$.ctx[9];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), y();
  }
  get elem_style() {
    return this.$$.ctx[10];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), y();
  }
}
export {
  H as default
};
