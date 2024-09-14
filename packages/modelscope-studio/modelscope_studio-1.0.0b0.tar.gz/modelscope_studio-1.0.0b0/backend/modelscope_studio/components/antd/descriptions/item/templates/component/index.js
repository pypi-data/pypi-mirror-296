function L(n) {
  const {
    gradio: t,
    _internal: s,
    ...i
  } = n;
  return Object.keys(s).reduce((l, e) => {
    const o = e.match(/bind_(.+)_event/);
    if (o) {
      const c = o[1], u = c.split("_"), a = (...m) => {
        const y = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
          type: f.type,
          detail: f.detail,
          timestamp: f.timeStamp,
          clientX: f.clientX,
          clientY: f.clientY,
          targetId: f.target.id,
          targetClassName: f.target.className,
          altKey: f.altKey,
          ctrlKey: f.ctrlKey,
          shiftKey: f.shiftKey,
          metaKey: f.metaKey
        } : f);
        return t.dispatch(c.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: y,
          component: i
        });
      };
      if (u.length > 1) {
        let m = {
          ...i.props[u[0]] || {}
        };
        l[u[0]] = m;
        for (let f = 1; f < u.length - 1; f++) {
          const h = {
            ...i.props[u[f]] || {}
          };
          m[u[f]] = h, m = h;
        }
        const y = u[u.length - 1];
        return m[`on${y.slice(0, 1).toUpperCase()}${y.slice(1)}`] = a, l;
      }
      const _ = u[0];
      l[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return l;
  }, {});
}
function v() {
}
function Z(n, t) {
  return n != n ? t == t : n !== t || n && typeof n == "object" || typeof n == "function";
}
function B(n, ...t) {
  if (n == null) {
    for (const i of t)
      i(void 0);
    return v;
  }
  const s = n.subscribe(...t);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function p(n) {
  let t;
  return B(n, (s) => t = s)(), t;
}
const g = [];
function b(n, t = v) {
  let s;
  const i = /* @__PURE__ */ new Set();
  function l(c) {
    if (Z(n, c) && (n = c, s)) {
      const u = !g.length;
      for (const a of i)
        a[1](), g.push(a, n);
      if (u) {
        for (let a = 0; a < g.length; a += 2)
          g[a][0](g[a + 1]);
        g.length = 0;
      }
    }
  }
  function e(c) {
    l(c(n));
  }
  function o(c, u = v) {
    const a = [c, u];
    return i.add(a), i.size === 1 && (s = t(l, e) || v), c(n), () => {
      i.delete(a), i.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: l,
    update: e,
    subscribe: o
  };
}
const {
  getContext: F,
  setContext: E
} = window.__gradio__svelte__internal, G = "$$ms-gr-antd-slots-key";
function H() {
  const n = b({});
  return E(G, n);
}
const J = "$$ms-gr-antd-context-key";
function Q(n) {
  var c;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = V(), s = $({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  t && t.subscribe((u) => {
    s.slotKey.set(u);
  }), T();
  const i = F(J), l = ((c = p(i)) == null ? void 0 : c.as_item) || n.as_item, e = i ? l ? p(i)[l] : p(i) : {}, o = b({
    ...n,
    ...e
  });
  return i ? (i.subscribe((u) => {
    const {
      as_item: a
    } = p(o);
    a && (u = u[a]), o.update((_) => ({
      ..._,
      ...u
    }));
  }), [o, (u) => {
    const a = u.as_item ? p(i)[u.as_item] : p(i);
    return o.set({
      ...u,
      ...a
    });
  }]) : [o, (u) => {
    o.set(u);
  }];
}
const M = "$$ms-gr-antd-slot-key";
function T() {
  E(M, b(void 0));
}
function V() {
  return F(M);
}
const W = "$$ms-gr-antd-component-slot-context-key";
function $({
  slot: n,
  index: t,
  subIndex: s
}) {
  return E(W, {
    slotKey: b(n),
    slotIndex: b(t),
    subSlotIndex: b(s)
  });
}
function tt(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
}
var z = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(n) {
  (function() {
    var t = {}.hasOwnProperty;
    function s() {
      for (var e = "", o = 0; o < arguments.length; o++) {
        var c = arguments[o];
        c && (e = l(e, i(c)));
      }
      return e;
    }
    function i(e) {
      if (typeof e == "string" || typeof e == "number")
        return e;
      if (typeof e != "object")
        return "";
      if (Array.isArray(e))
        return s.apply(null, e);
      if (e.toString !== Object.prototype.toString && !e.toString.toString().includes("[native code]"))
        return e.toString();
      var o = "";
      for (var c in e)
        t.call(e, c) && e[c] && (o = l(o, c));
      return o;
    }
    function l(e, o) {
      return o ? e ? e + " " + o : e + o : e;
    }
    n.exports ? (s.default = s, n.exports = s) : window.classNames = s;
  })();
})(z);
var et = z.exports;
const nt = /* @__PURE__ */ tt(et), {
  getContext: st,
  setContext: it
} = window.__gradio__svelte__internal;
function lt(n) {
  const t = `$$ms-gr-antd-${n}-context-key`;
  function s(l = ["default"]) {
    const e = l.reduce((o, c) => (o[c] = b([]), o), {});
    return it(t, {
      itemsMap: e,
      allowedSlots: l
    }), e;
  }
  function i() {
    const {
      itemsMap: l,
      allowedSlots: e
    } = st(t);
    return function(o, c, u) {
      l && (o ? l[o].update((a) => {
        const _ = [...a];
        return e.includes(o) ? _[c] = u : _[c] = void 0, _;
      }) : e.includes("default") && l.default.update((a) => {
        const _ = [...a];
        return _[c] = u, _;
      }));
    };
  }
  return {
    getItems: s,
    getSetItemFn: i
  };
}
const {
  getItems: Kt,
  getSetItemFn: ot
} = lt("descriptions"), {
  SvelteComponent: rt,
  binding_callbacks: ct,
  check_outros: ut,
  component_subscribe: x,
  create_slot: ft,
  detach: R,
  element: at,
  empty: _t,
  flush: d,
  get_all_dirty_from_scope: mt,
  get_slot_changes: dt,
  group_outros: bt,
  init: yt,
  insert: U,
  safe_not_equal: ht,
  set_custom_element_data: pt,
  transition_in: k,
  transition_out: P,
  update_slot_base: gt
} = window.__gradio__svelte__internal;
function A(n) {
  let t, s;
  const i = (
    /*#slots*/
    n[20].default
  ), l = ft(
    i,
    n,
    /*$$scope*/
    n[19],
    null
  );
  return {
    c() {
      t = at("svelte-slot"), l && l.c(), pt(t, "class", "svelte-8w4ot5");
    },
    m(e, o) {
      U(e, t, o), l && l.m(t, null), n[21](t), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      524288) && gt(
        l,
        i,
        e,
        /*$$scope*/
        e[19],
        s ? dt(
          i,
          /*$$scope*/
          e[19],
          o,
          null
        ) : mt(
          /*$$scope*/
          e[19]
        ),
        null
      );
    },
    i(e) {
      s || (k(l, e), s = !0);
    },
    o(e) {
      P(l, e), s = !1;
    },
    d(e) {
      e && R(t), l && l.d(e), n[21](null);
    }
  };
}
function xt(n) {
  let t, s, i = (
    /*$mergedProps*/
    n[1].visible && A(n)
  );
  return {
    c() {
      i && i.c(), t = _t();
    },
    m(l, e) {
      i && i.m(l, e), U(l, t, e), s = !0;
    },
    p(l, [e]) {
      /*$mergedProps*/
      l[1].visible ? i ? (i.p(l, e), e & /*$mergedProps*/
      2 && k(i, 1)) : (i = A(l), i.c(), k(i, 1), i.m(t.parentNode, t)) : i && (bt(), P(i, 1, 1, () => {
        i = null;
      }), ut());
    },
    i(l) {
      s || (k(i), s = !0);
    },
    o(l) {
      P(i), s = !1;
    },
    d(l) {
      l && R(t), i && i.d(l);
    }
  };
}
function Ct(n, t, s) {
  let i, l, e, o, c, {
    $$slots: u = {},
    $$scope: a
  } = t, {
    gradio: _
  } = t, {
    props: m = {}
  } = t;
  const y = b(m);
  x(n, y, (r) => s(18, c = r));
  let {
    _internal: f = {}
  } = t, {
    label: h
  } = t, {
    as_item: C
  } = t, {
    visible: K = !0
  } = t, {
    elem_id: S = ""
  } = t, {
    elem_classes: w = []
  } = t, {
    elem_style: I = {}
  } = t;
  const j = b();
  x(n, j, (r) => s(0, l = r));
  const N = V();
  x(n, N, (r) => s(17, o = r));
  const [O, X] = Q({
    gradio: _,
    props: c,
    _internal: f,
    visible: K,
    elem_id: S,
    elem_classes: w,
    elem_style: I,
    as_item: C,
    label: h
  });
  x(n, O, (r) => s(1, e = r));
  const q = H();
  x(n, q, (r) => s(16, i = r));
  const Y = ot();
  function D(r) {
    ct[r ? "unshift" : "push"](() => {
      l = r, j.set(l);
    });
  }
  return n.$$set = (r) => {
    "gradio" in r && s(7, _ = r.gradio), "props" in r && s(8, m = r.props), "_internal" in r && s(9, f = r._internal), "label" in r && s(10, h = r.label), "as_item" in r && s(11, C = r.as_item), "visible" in r && s(12, K = r.visible), "elem_id" in r && s(13, S = r.elem_id), "elem_classes" in r && s(14, w = r.elem_classes), "elem_style" in r && s(15, I = r.elem_style), "$$scope" in r && s(19, a = r.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*props*/
    256 && y.update((r) => ({
      ...r,
      ...m
    })), n.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, label*/
    327296 && X({
      gradio: _,
      props: c,
      _internal: f,
      visible: K,
      elem_id: S,
      elem_classes: w,
      elem_style: I,
      as_item: C,
      label: h
    }), n.$$.dirty & /*$slotKey, $mergedProps, $slot, $slots*/
    196611 && Y(o, e._internal.index || 0, {
      props: {
        style: e.elem_style,
        className: nt(e.elem_classes, "ms-gr-antd-descriptions-item"),
        id: e.elem_id,
        label: e.label,
        ...e.props,
        ...L(e)
      },
      slots: {
        children: l,
        ...i
      }
    });
  }, [l, e, y, j, N, O, q, _, m, f, h, C, K, S, w, I, i, o, c, a, u, D];
}
class St extends rt {
  constructor(t) {
    super(), yt(this, t, Ct, xt, ht, {
      gradio: 7,
      props: 8,
      _internal: 9,
      label: 10,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), d();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), d();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), d();
  }
  get label() {
    return this.$$.ctx[10];
  }
  set label(t) {
    this.$$set({
      label: t
    }), d();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), d();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), d();
  }
}
export {
  St as default
};
